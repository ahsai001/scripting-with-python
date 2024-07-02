import 'package:envied/envied.dart';

part 'env.g.dart';

@Envied(path: '.env', obfuscate: true)
abstract class Env {
  @EnviedField(varName: "API_KEY")
  static final String apiKey = _Env.apiKey;

  @EnviedField(varName: "API_PROTOCOL")
  static final String apiProtocol = _Env.apiProtocol;

  @EnviedField(varName: "API_ENDPOINTS")
  static final String apiEndPoints = _Env.apiEndPoints;
}
