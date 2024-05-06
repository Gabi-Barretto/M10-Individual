import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class RegisterPage extends StatefulWidget {
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();

  Future<void> registerUser() async {
    final url = Uri.parse('http://10.0.2.2:5000/register');
    final headers = <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    };
    final body = jsonEncode({
      'name': _usernameController.text,
      'password': _passwordController.text,
      'email': _emailController.text,
    });

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode == 200) {
      print('Usuário registrado com sucesso');
    } else {
      print('Erro no registro: ${response.statusCode} - ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Register')),
      body: Column(
        children: <Widget>[
          TextField(controller: _usernameController, decoration: InputDecoration(labelText: 'Username')),
          TextField(controller: _passwordController, decoration: InputDecoration(labelText: 'Password'), obscureText: true),
          TextField(controller: _emailController, decoration: InputDecoration(labelText: 'Email')),
          ElevatedButton(onPressed: registerUser, child: Text('Register'))
        ],
      ),
    );
  }
}
