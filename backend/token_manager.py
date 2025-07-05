#!/usr/bin/env python3
"""
eBay OAuth Token Manager
Utility script to help manage OAuth tokens for the eBay API.
"""

import os
import requests
from dotenv import load_dotenv
import click
from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()


def get_auth_url(client_id: str, redirect_uri: str, environment: str = "production") -> str:
    """Generate the authorization URL for OAuth flow."""
    base_url = "https://auth.ebay.com" if environment == "production" else "https://auth.sandbox.ebay.com"
    
    scopes = [
        "https://api.ebay.com/oauth/api_scope",
        "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "https://api.ebay.com/oauth/api_scope/sell.account"
    ]
    
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "prompt": "login"
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}/oauth2/authorize?{query_string}"


def exchange_code_for_token(client_id: str, client_secret: str, auth_code: str, 
                           redirect_uri: str, environment: str = "production") -> dict:
    """Exchange authorization code for access and refresh tokens."""
    token_url = (
        "https://api.ebay.com/identity/v1/oauth2/token"
        if environment == "production"
        else "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    )
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }
    
    auth = (client_id, client_secret)
    
    response = requests.post(token_url, headers=headers, auth=auth, data=data)
    response.raise_for_status()
    
    return response.json()


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str, 
                        environment: str = "production") -> dict:
    """Refresh access token using refresh token."""
    token_url = (
        "https://api.ebay.com/identity/v1/oauth2/token"
        if environment == "production"
        else "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    )
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account"
    }
    
    auth = (client_id, client_secret)
    
    response = requests.post(token_url, headers=headers, auth=auth, data=data)
    response.raise_for_status()
    
    return response.json()


@click.group()
def cli():
    """eBay OAuth Token Manager - Manage your eBay API tokens."""
    pass


@cli.command()
@click.option('--client-id', envvar='EBAY_CLIENT_ID', help='eBay Client ID')
@click.option('--redirect-uri', envvar='EBAY_REDIRECT_URI', help='eBay Redirect URI')
@click.option('--environment', default='production', type=click.Choice(['production', 'sandbox']), 
              help='eBay environment')
def auth_url(client_id: str, redirect_uri: str, environment: str):
    """Generate authorization URL for OAuth flow."""
    if not client_id or not redirect_uri:
        console.print("[red]Error: Client ID and Redirect URI are required[/red]")
        return
    
    auth_url_str = get_auth_url(client_id, redirect_uri, environment)
    
    console.print(Panel.fit(
        f"[bold blue]eBay Authorization URL[/bold blue]\n\n"
        f"[yellow]Environment:[/yellow] {environment}\n"
        f"[yellow]Client ID:[/yellow] {client_id}\n"
        f"[yellow]Redirect URI:[/yellow] {redirect_uri}\n\n"
        f"[green]Authorization URL:[/green]\n"
        f"{auth_url_str}\n\n"
        f"[cyan]Instructions:[/cyan]\n"
        f"1. Open this URL in your browser\n"
        f"2. Log in to your eBay account\n"
        f"3. Authorize the application\n"
        f"4. Copy the authorization code from the redirect URL\n"
        f"5. Use the 'exchange-token' command to get your tokens",
        border_style="blue"
    ))


@cli.command()
@click.option('--client-id', envvar='EBAY_CLIENT_ID', help='eBay Client ID')
@click.option('--client-secret', envvar='EBAY_CLIENT_SECRET', help='eBay Client Secret')
@click.option('--auth-code', help='Authorization code from OAuth flow')
@click.option('--redirect-uri', envvar='EBAY_REDIRECT_URI', help='eBay Redirect URI')
@click.option('--environment', default='production', type=click.Choice(['production', 'sandbox']), 
              help='eBay environment')
def exchange_token(client_id: str, client_secret: str, auth_code: str, redirect_uri: str, environment: str):
    """Exchange authorization code for access and refresh tokens."""
    if not all([client_id, client_secret, auth_code, redirect_uri]):
        console.print("[red]Error: Client ID, Client Secret, Auth Code, and Redirect URI are required[/red]")
        return
    
    try:
        token_data = exchange_code_for_token(client_id, client_secret, auth_code, redirect_uri, environment)
        
        console.print(Panel.fit(
            f"[bold green]Token Exchange Successful![/bold green]\n\n"
            f"[yellow]Environment:[/yellow] {environment}\n"
            f"[yellow]Access Token:[/yellow] {token_data.get('access_token', 'N/A')[:20]}...\n"
            f"[yellow]Refresh Token:[/yellow] {token_data.get('refresh_token', 'N/A')[:20]}...\n"
            f"[yellow]Expires In:[/yellow] {token_data.get('expires_in', 'N/A')} seconds\n"
            f"[yellow]Token Type:[/yellow] {token_data.get('token_type', 'N/A')}\n\n"
            f"[cyan]Add these to your .env file:[/cyan]\n"
            f"EBAY_REFRESH_TOKEN={token_data.get('refresh_token', '')}\n"
            f"EBAY_ENVIRONMENT={environment}",
            border_style="green"
        ))
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error exchanging token: {e}[/red]")


@cli.command()
@click.option('--client-id', envvar='EBAY_CLIENT_ID', help='eBay Client ID')
@click.option('--client-secret', envvar='EBAY_CLIENT_SECRET', help='eBay Client Secret')
@click.option('--refresh-token', envvar='EBAY_REFRESH_TOKEN', help='eBay Refresh Token')
@click.option('--environment', default='production', type=click.Choice(['production', 'sandbox']), 
              help='eBay environment')
def refresh_token(client_id: str, client_secret: str, refresh_token: str, environment: str):
    """Refresh access token using refresh token."""
    if not all([client_id, client_secret, refresh_token]):
        console.print("[red]Error: Client ID, Client Secret, and Refresh Token are required[/red]")
        return
    
    try:
        token_data = refresh_access_token(client_id, client_secret, refresh_token, environment)
        
        console.print(Panel.fit(
            f"[bold green]Token Refresh Successful![/bold green]\n\n"
            f"[yellow]Environment:[/yellow] {environment}\n"
            f"[yellow]New Access Token:[/yellow] {token_data.get('access_token', 'N/A')[:20]}...\n"
            f"[yellow]New Refresh Token:[/yellow] {token_data.get('refresh_token', 'N/A')[:20]}...\n"
            f"[yellow]Expires In:[/yellow] {token_data.get('expires_in', 'N/A')} seconds\n"
            f"[yellow]Token Type:[/yellow] {token_data.get('token_type', 'N/A')}\n\n"
            f"[cyan]Update your .env file with the new refresh token if provided.[/cyan]",
            border_style="green"
        ))
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error refreshing token: {e}[/red]")


@cli.command()
def setup():
    """Interactive setup for eBay OAuth credentials."""
    console.print(Panel.fit(
        "[bold blue]eBay OAuth Setup Guide[/bold blue]\n\n"
        "1. Go to https://developer.ebay.com/my/keys\n"
        "2. Create a new application or use existing one\n"
        "3. Note your Client ID and Client Secret\n"
        "4. Set your Redirect URI (e.g., https://localhost:8080/callback)\n"
        "5. Use the 'auth-url' command to get authorization URL\n"
        "6. Complete OAuth flow and get authorization code\n"
        "7. Use 'exchange-token' to get access and refresh tokens\n"
        "8. Add tokens to your .env file\n\n"
        "[yellow]Required .env variables:[/yellow]\n"
        "EBAY_CLIENT_ID=your_client_id\n"
        "EBAY_CLIENT_SECRET=your_client_secret\n"
        "EBAY_REDIRECT_URI=your_redirect_uri\n"
        "EBAY_REFRESH_TOKEN=your_refresh_token\n"
        "EBAY_ENVIRONMENT=production",
        border_style="blue"
    ))


if __name__ == "__main__":
    cli() 