import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ContentPage extends StatefulWidget {
  const ContentPage({super.key});

  @override
  _ContentPageState createState() => _ContentPageState();
}

class _ContentPageState extends State<ContentPage> {
  String imageUrl = "https://picsum.photos/300";
  File? _image;
  String? _processedImageUrl;
  final ImagePicker _picker = ImagePicker();

  void _refreshImage() {
    setState(() {
      imageUrl = "https://picsum.photos/300?random=${DateTime.now().millisecondsSinceEpoch}";
    });
  }

  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
        _processedImageUrl = null;  // Reset processed image when a new image is picked
      });

      await _uploadImage(_image!);
    }
  }

  Future<void> _uploadImage(File image) async {
    final request = http.MultipartRequest('POST', Uri.parse('http://10.0.2.2:8003/image/remove-background'));
    request.files.add(await http.MultipartFile.fromPath('file', image.path));

    try {
      final response = await request.send();

      if (response.statusCode == 200) {
        final responseData = await response.stream.bytesToString();
        final responseBody = jsonDecode(responseData);
        final base64Image = responseBody['base64_image'];

        setState(() {
          _processedImageUrl = base64Image;
        });
      } else {
        final responseData = await response.stream.bytesToString();
        final responseBody = jsonDecode(responseData);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Falha ao fazer upload da imagem: ${responseBody['detail']}')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erro no upload da imagem: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    // Defina o tamanho máximo para a imagem processada
    final double maxImageHeight = MediaQuery.of(context).size.height * 0.4; // 40% da altura da tela

    return Scaffold(
      appBar: AppBar(
        title: const Text('Conteúdo Secreto'),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              const SizedBox(height: 20),
              SizedBox(
                width: maxImageHeight, // Largura proporcional à altura
                height: maxImageHeight, // Altura proporcional à tela
                child: Image.network(
                  imageUrl,
                  key: ValueKey(imageUrl),
                  fit: BoxFit.cover,
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _refreshImage,
                child: const Text('Refresh Page'),
              ),
              const SizedBox(height: 20),
              if (_processedImageUrl != null)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Image.memory(
                    base64Decode(_processedImageUrl!),
                    fit: BoxFit.contain,
                    height: maxImageHeight, // Manter a lógica proporcional
                  ),
                ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _pickImage,
                child: const Text('Upload Image'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
