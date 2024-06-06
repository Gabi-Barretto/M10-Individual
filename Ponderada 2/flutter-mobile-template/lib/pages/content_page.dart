import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ContentPage extends StatefulWidget {
  @override
  _ContentPageState createState() => _ContentPageState();
}

class _ContentPageState extends State<ContentPage> {
  String imageUrl = "https://picsum.photos/300";
  File? _image;
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
      });

      await _uploadImage(_image!);
    }
  }

  Future<void> _uploadImage(File image) async {
    final bytes = await image.readAsBytes();
    String base64Image = base64Encode(bytes);

    final response = await http.post(
      Uri.parse('http://seu-backend.com/remove-bg'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'base64_image': base64Image,
      }),
    );

    if (response.statusCode == 200) {
      final responseBody = jsonDecode(response.body);
      setState(() {
        imageUrl = 'data:image/png;base64,${responseBody['base64_image']}';
      });
    } else {
      throw Exception('Failed to upload image');
    }
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
            _image == null
                ? Image.network(
                    imageUrl,
                    key: ValueKey(imageUrl),
                  )
                : Image.file(_image!),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _refreshImage,
              child: const Text('Refresh Page'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: const Text('Upload Image'),
            ),
          ],
        ),
      ),
    );
  }
}
