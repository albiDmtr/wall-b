import { NextRequest, NextResponse } from "next/server";

export interface RobotCommand {
  type: "move" | "speak" | "standby" | "action" | "status";
  angle?: number;
  text?: string;
  action?: string;
  status?: string;
  timestamp?: number;
}

let currentCommand: RobotCommand | null = {
  type: "standby",
  timestamp: Date.now(),
};

// Store active connections
const clients = new Set<ReadableStreamDefaultController>();

export async function GET(request: NextRequest) {
  let controller: ReadableStreamDefaultController;
  let interval: NodeJS.Timeout;

  const stream = new ReadableStream({
    start(ctrl) {
      controller = ctrl; // Store reference for cleanup

      // Send standby command immediately
      const data = `data: ${JSON.stringify({ type: "standby", timestamp: Date.now() })}\n\n`;
      controller.enqueue(new TextEncoder().encode(data));

      // Send periodic updates
      interval = setInterval(() => {
        try {
          if (currentCommand) {
            const data = `data: ${JSON.stringify(currentCommand)}\n\n`;
            controller.enqueue(new TextEncoder().encode(data));

            currentCommand = null;
          }

          // Only send speak and action commands once
        } catch (error) {
          clearInterval(interval);
          try {
            controller.close();
          } catch {}
        }
      }, 50);

      // Cleanup on connection close
      request.signal.addEventListener("abort", () => {
        clearInterval(interval);
        try {
          controller.close();
        } catch {}
      });
    },

    cancel() {
      clearInterval(interval);
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
    const body: RobotCommand = await request.json();
    const { type, angle, text, action, status } = body;

    // Validate wheel states
    const validTypes = [
      "move",
      "speak",
      "standby",
      "action",
      "status",
    ] as const;
    if (!validTypes.includes(type)) {
      return NextResponse.json(
        { error: "Invalid command type." },
        { status: 400 },
      );
    }

    // Update current command
    currentCommand = {
      type: type,
      timestamp: Date.now(),
    };
    if (type === "move") {
      currentCommand.angle = angle;
    } else if (type === "speak") {
      currentCommand.text = text;
    } else if (type === "action") {
      currentCommand.action = action;
      currentCommand.text = text;
    } else if (type === "status") {
      currentCommand.status = status;
    }

    return NextResponse.json({
      success: true,
      command: currentCommand,
    });
  } catch (error) {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
}
