import 'package:flutter/material.dart';

class ContentPage extends StatefulWidget {
  @override
  _ContentPageState createState() => _ContentPageState();
}

class _ContentPageState extends State<ContentPage> {
  String imageUrl = "https://picsum.photos/300";

  void _refreshImage() {
    setState(() {
      // Adiciona um parâmetro de query timestamp à URL para forçar uma nova carga
      imageUrl = "https://picsum.photos/300?random=${DateTime.now().millisecondsSinceEpoch}";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Conteúdo Secreto'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Conteúdo Secreto',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            Image.network(
              imageUrl,
              key: ValueKey(imageUrl), // Usa a URL atualizada como key
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _refreshImage,
              child: const Text('Refresh Page'),
            ),
          ],
        ),
      ),
    );
  }
}