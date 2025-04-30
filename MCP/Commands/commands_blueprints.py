"""Blueprint-related commands for Unreal Engine.

This module contains all blueprint-related commands for the UnrealMCP bridge,
including creation, modification, and querying of blueprints.
"""

import sys
import os
from mcp.server.fastmcp import Context

# Import send_command from the parent module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unreal_mcp_bridge import send_command

def register_all(mcp):
    """Register all blueprint-related commands with the MCP server."""
    
    @mcp.tool()
    def create_blueprint(ctx: Context, package_path: str, name: str, parent_class: str = "Actor", properties: dict = None) -> str:
        """Create a new blueprint in the Unreal project.
        
        Args:
            package_path: The path where the blueprint should be created (e.g., '/Game/Blueprints')
            name: The name of the blueprint
            parent_class: The parent class of the blueprint (default: 'Actor')
            properties: Optional dictionary of blueprint properties to set.
        """
        try:
            params = {
                "package_path": package_path,
                "name": name,
                "parent_class": parent_class
            }
            if properties:
                params["properties"] = properties
            response = send_command("create_blueprint", params)
            if response["status"] == "success":
                return f"Created blueprint: {response['result']['name']} at path: {response['result']['path']}"
            else:
                return f"Error: {response['message']}"
        except Exception as e:
            return f"Error creating blueprint: {str(e)}"

    @mcp.tool()
    def modify_blueprint(ctx: Context, blueprint_path: str, properties: dict) -> str:
        """Modify an existing blueprint's properties.
        
        Args:
            blueprint_path: The full path to the blueprint (e.g., '/Game/Blueprints/MyBlueprint')
            properties: Dictionary of blueprint properties to set.
        """
        try:
            params = {
                "blueprint_path": blueprint_path,
                "properties": properties
            }
            response = send_command("modify_blueprint", params)
            if response["status"] == "success":
                return f"Modified blueprint: {response['result']['name']} at path: {response['result']['path']}"
            else:
                return f"Error: {response['message']}"
        except Exception as e:
            return f"Error modifying blueprint: {str(e)}"

    @mcp.tool()
    def get_blueprint_info(ctx: Context, blueprint_path: str) -> dict:
        """Get information about a blueprint.
        
        Args:
            blueprint_path: The full path to the blueprint (e.g., '/Game/Blueprints/MyBlueprint')
            
        Returns:
            Dictionary containing blueprint information.
        """
        try:
            params = {"blueprint_path": blueprint_path}
            response = send_command("get_blueprint_info", params)
            if response["status"] == "success":
                return response["result"]
            else:
                return {"error": response["message"]}
        except Exception as e:
            return {"error": str(e)}
