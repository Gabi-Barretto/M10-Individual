import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';

class ContentPage extends StatefulWidget {
  const ContentPage({super.key});

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
    // Solicitar permissão de armazenamento
    if (await Permission.storage.request().isGranted) {
      final pickedFile = await _picker.pickImage(source: ImageSource.gallery);

      if (pickedFile != null) {
        setState(() {
          _image = File(pickedFile.path);
        });

        await _uploadImage(_image!);
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Permissão de armazenamento negada')),
      );
    }
  }

  Future<void> _uploadImage(File image) async {
    final request = http.MultipartRequest('POST', Uri.parse('http://10.0.2.2:8003/image/remove-background'));
    request.files.add(await http.MultipartFile.fromPath('file', image.path));

    final response = await request.send();

    if (response.statusCode == 200) {
      final responseData = await response.stream.bytesToString();
      final responseBody = jsonDecode(responseData);
      final base64Image = responseBody['base64_image'];

      // Decode the base64 image
      final bytes = base64Decode(base64Image);

      // Get the application documents directory
      final directory = await getExternalStorageDirectory();
      if (directory != null) {
        final filePath = '${directory.path}/processed_image.png';

        // Save the image as a file
        final file = File(filePath);
        await file.writeAsBytes(bytes);

        // Notify the user
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Imagem salva em $filePath')),
        );
      }
    } else {
      print('Failed to upload image: ${response.statusCode}');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Falha ao fazer upload da imagem')),
      );
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
