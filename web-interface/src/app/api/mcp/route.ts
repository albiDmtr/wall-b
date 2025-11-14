import { NextRequest, NextResponse } from "next/server";

export interface McpCommand {
  type: "ping" | "plan";
  text?: string;
  timestamp?: number;
}

// Store active connections
const clients = new Set<ReadableStreamDefaultController>();

// Helper to broadcast messages to all connected clients
function broadcast(command: McpCommand) {
  const message = `data: ${JSON.stringify(command)}\n\n`;

  clients.forEach((controller) => {
    try {
      controller.enqueue(new TextEncoder().encode(message));
    } catch (error) {
      // Client disconnected, remove it
      clients.delete(controller);
    }
  });
}

export async function GET(request: NextRequest) {
  let controller: ReadableStreamDefaultController;
  let keepAliveInterval: NodeJS.Timeout;

  const stream = new ReadableStream({
    start(ctrl) {
      controller = ctrl;

      // Add this client to the set
      clients.add(controller);

      // Send initial connection message
      const connectMsg = `data: ${JSON.stringify({ type: "ping", timestamp: Date.now() })}\n\n`;
      controller.enqueue(new TextEncoder().encode(connectMsg));

      // Keep-alive ping every 30 seconds
      keepAliveInterval = setInterval(() => {
        try {
          const pingMsg = `data: ${JSON.stringify({ type: "ping", timestamp: Date.now() })}\n\n`;
          controller.enqueue(new TextEncoder().encode(pingMsg));
        } catch {
          clearInterval(keepAliveInterval);
          clients.delete(controller);
        }
      }, 30000);

      // Cleanup on connection close
      request.signal.addEventListener("abort", () => {
        clearInterval(keepAliveInterval);
        clients.delete(controller);
        try {
          controller.close();
        } catch {}
      });
    },
    cancel() {
      clearInterval(keepAliveInterval);
      clients.delete(controller);
      try {
        controller.close();
      } catch {}
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
      "Access-Control-Allow-Origin": "*",
    },
  });
}

export async function POST(request: NextRequest) {
  try {
    const body: any = await request.json();
    const { type, text } = body;

    const command: McpCommand = {
      type,
      text,
      timestamp: Date.now(),
    };

    // Broadcast to all connected SSE clients
    broadcast(command);

    return NextResponse.json({
      success: true,
      clientCount: clients.size,
    });
  } catch (error) {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
}
