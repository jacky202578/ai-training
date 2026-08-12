<?php
// AI交付管理能力培训 — 学习进度API
// GET  ?uid=xxx → 返回进度
// POST body:{uid,lesson_id,data} → 保存进度

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

$usersDir = __DIR__ . '/users/';
if (!is_dir($usersDir)) { mkdir($usersDir, 0755, true); }

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $uid = isset($_GET['uid']) ? preg_replace('/[^a-zA-Z0-9_-]/', '', $_GET['uid']) : 'guest';
    $file = $usersDir . $uid . '.json';
    
    if (file_exists($file)) {
        echo file_get_contents($file);
    } else {
        echo json_encode(['uid' => $uid, 'lessons' => new stdClass(), 'total_time' => 0]);
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input) { http_response_code(400); echo json_encode(['error' => 'invalid json']); exit; }
    
    $uid = isset($input['uid']) ? preg_replace('/[^a-zA-Z0-9_-]/', '', $input['uid']) : 'guest';
    $lessonId = isset($input['lesson_id']) ? preg_replace('/[^a-zA-Z0-9_-]/', '', $input['lesson_id']) : '';
    $data = isset($input['data']) ? $input['data'] : [];
    
    $file = $usersDir . $uid . '.json';
    $userData = ['uid' => $uid, 'lessons' => new stdClass(), 'total_time' => 0];
    
    if (file_exists($file)) {
        $userData = json_decode(file_get_contents($file), true);
    }
    
    if ($lessonId) {
        if (!isset($userData['lessons'][$lessonId])) {
            $userData['lessons'][$lessonId] = [];
        }
        foreach ($data as $k => $v) {
            $userData['lessons'][$lessonId][$k] = $v;
        }
    }
    
    if (isset($data['completed_at'])) {
        $userData['total_time'] = ($userData['total_time'] ?? 0) + 60;
    }
    
    file_put_contents($file, json_encode($userData, JSON_UNESCAPED_UNICODE), LOCK_EX);
    echo json_encode(['ok' => true]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'method not allowed']);
