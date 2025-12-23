import 'package:dio/dio.dart';

class DioClient {
  static final DioClient _singleton = DioClient._internal();
  late final Dio _dio;

  factory DioClient() {
    return _singleton;
  }

  DioClient._internal() {
    _dio = Dio(
      BaseOptions(
        // Android Emülatör için 10.0.2.2, Gerçek cihaz için bilgisayarın yerel IP'si (örn. 192.168.1.X)
      baseUrl: 'http://10.0.2.2:8000/api/v1',
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
      ),
    );
    
    // Loglama için interceptor ekleyebiliriz
    _dio.interceptors.add(LogInterceptor(
      request: true,
      requestHeader: true,
      requestBody: true,
      responseHeader: true,
      responseBody: true,
      error: true,
    ));
  }

  Dio get dio => _dio;
}
