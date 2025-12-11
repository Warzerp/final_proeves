#!/usr/bin/env python
"""
SmartHealth WebSocket Test Script
Tests the WebSocket functionality
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime


class WebSocketTester:
    def __init__(self, uri="ws://localhost:8000/ws/chat"):
        self.uri = uri
        self.websocket = None
        self.test_results = []
        
    async def connect(self):
        """Establecer conexión WebSocket"""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.log_result("Connection", True, "WebSocket conectado exitosamente")
            return True
        except Exception as e:
            self.log_result("Connection", False, str(e))
            return False
    
    async def disconnect(self):
        """Cerrar conexión WebSocket"""
        if self.websocket:
            await self.websocket.close()
            self.log_result("Disconnection", True, "WebSocket desconectado")
    
    async def send_message(self, message):
        """Enviar mensaje por WebSocket"""
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            await self.websocket.send(message)
            return True
        except Exception as e:
            self.log_result("Send Message", False, str(e))
            return False
    
    async def receive_message(self, timeout=5):
        """Recibir mensaje del WebSocket"""
        try:
            message = await asyncio.wait_for(self.websocket.recv(), timeout=timeout)
            return json.loads(message) if isinstance(message, str) else message
        except asyncio.TimeoutError:
            self.log_result("Receive Message", False, "Timeout esperando mensaje")
            return None
        except Exception as e:
            self.log_result("Receive Message", False, str(e))
            return None
    
    async def test_message_format(self):
        """Test formato de mensajes"""
        test_message = {
            "type": "query",
            "data": {
                "patient_id": "12345",
                "question": "¿Cuál es el diagnóstico?"
            }
        }
        
        if await self.send_message(test_message):
            response = await self.receive_message()
            if response:
                self.log_result("Message Format", True, "Formato de mensaje válido")
            else:
                self.log_result("Message Format", False, "No se recibió respuesta")
    
    async def test_authentication(self):
        """Test autenticación"""
        auth_message = {
            "type": "authenticate",
            "token": "mock_jwt_token_12345"
        }
        
        if await self.send_message(auth_message):
            response = await self.receive_message()
            if response:
                self.log_result("Authentication", True, "Autenticación procesada")
            else:
                self.log_result("Authentication", False, "Fallo en autenticación")
    
    async def test_latency(self):
        """Test latencia de respuesta"""
        start_time = datetime.now()
        
        ping_message = {"type": "ping"}
        if await self.send_message(ping_message):
            response = await self.receive_message()
            if response:
                latency = (datetime.now() - start_time).total_seconds() * 1000
                self.log_result("Latency", True, f"Latencia: {latency:.2f}ms")
            else:
                self.log_result("Latency", False, "No se recibió pong")
    
    def log_result(self, test_name, passed, message):
        """Registrar resultado de prueba"""
        result = {
            "test": test_name,
            "passed": passed,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}: {message}")
    
    def print_summary(self):
        """Mostrar resumen de pruebas"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = total - passed
        
        print("\n" + "="*50)
        print("Resumen de Pruebas WebSocket")
        print("="*50)
        print(f"Total de pruebas: {total}")
        print(f"Pasadas: {passed}")
        print(f"Falló: {failed}")
        print(f"Tasa de éxito: {(passed/total*100):.1f}%")
        print("="*50 + "\n")
    
    async def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("\nIniciando pruebas WebSocket...\n")
        
        if not await self.connect():
            print("No se pudo conectar al WebSocket")
            return
        
        try:
            await self.test_message_format()
            await self.test_authentication()
            await self.test_latency()
        finally:
            await self.disconnect()
        
        self.print_summary()


async def main():
    """Función principal"""
    tester = WebSocketTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPruebas interrumpidas por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
