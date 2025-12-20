import 'package:flutter/material.dart';

class HomeView extends StatelessWidget {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Engelsiz Alışveriş'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Text(
              'Merhaba, Engelsiz Alışveriş!',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            Text('Kamera ve ses özellikleri burada olacak.'),
          ],
        ),
      ),
    );
  }
}
