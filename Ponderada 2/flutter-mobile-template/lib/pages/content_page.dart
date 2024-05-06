import 'package:flutter/material.dart';

class ContentPage extends StatefulWidget {
  @override
  _ContentPageState createState() => _ContentPageState();
}

class _ContentPageState extends State<ContentPage> {
  final String imageUrl = "https://picsum.photos/300";

  void _refreshImage() {
    setState(() {
      // This changes the key of the Image widget, forcing it to reload.
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
              key: ValueKey(DateTime.now().millisecondsSinceEpoch), // Force re-render
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
