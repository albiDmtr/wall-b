import { NextRequest, NextResponse } from "next/server";

// Initialize MCPControl to false
let MCPControl: boolean = false;

// GET endpoint to return the current value of MCPControl
export async function GET(request: NextRequest) {
  return NextResponse.json({ MCPControl });
}

// POST endpoint to update the value of MCPControl
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Check if MCPControl property exists in the request body
    if (typeof body.MCPControl === "undefined") {
      return NextResponse.json(
        { error: "MCPControl parameter is required" },
        { status: 400 },
      );
    }

    // Validate that MCPControl is a boolean
    if (typeof body.MCPControl !== "boolean") {
      return NextResponse.json(
        { error: "MCPControl must be a boolean value" },
        { status: 400 },
      );
    }

    // Update the MCPControl value
    MCPControl = body.MCPControl;

    return NextResponse.json({
      success: true,
      MCPControl,
    });
  } catch (error) {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
}
