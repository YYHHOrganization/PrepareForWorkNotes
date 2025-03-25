### 一、RPC 的核心概念
**RPC（Remote Procedure Call，远程过程调用）** 是一种计算机通信协议，允许程序像调用本地方法一样调用远程服务器的函数，底层隐藏了网络通信细节。其核心特性如下：

---

#### 1.1 工作原理
```python
# 伪代码示例：客户端调用远程的"玩家升级"方法
result = rpc_client.call("PlayerService.level_up", player_id=1001, exp=500)

# 实际执行流程：
1. 客户端序列化参数（player_id, exp）→ 二进制数据  # protobuf
2. 通过TCP/UDP发送到游戏服务器
3. 服务端反序列化数据 → 执行真实的level_up逻辑
4. 将结果（新等级）序列化后返回客户端
5. 客户端反序列化结果 → 更新本地界面
```

#### 1.2 与普通HTTP API的区别
| 特性     | RPC                      | HTTP API             |
| -------- | ------------------------ | -------------------- |
| 通信协议 | 自定义二进制协议         | HTTP/HTTPS           |
| 性能     | 高吞吐、低延迟（毫秒级） | 相对较低（文本协议） |
| 服务发现 | 集成注册中心             | 依赖DNS或网关        |
| 适用场景 | 内部微服务通信           | 对外暴露接口         |

---

### 二、游戏开发中的典型应用场景
#### 2.1 开放世界游戏（如《原神》）
- **动态场景同步**：
  ```java
  // 玩家A在蒙德城释放技能，同步给周围玩家
  rpcClient.invoke("SceneSync.broadcastSkill", 
    skillId=203, 
    position=Vector3(120,30,80), 
    targets=[enemy001, enemy002]
  );
  ```
  - **技术细节**：使用UDP协议 + 快照插值，减少延迟抖动

- **无缝地图加载**：
  ```csharp
  // 客户端预加载璃月地区资源
  bool success = await rpc.CallAsync("WorldStreaming.preloadRegion", "Liyue");
  if(success) EnterRegion("Liyue");
  ```

#### 2.2 回合制游戏（如《阴阳师》）
- **战斗逻辑验证**：
  ```python
  # 客户端发起"式神释放大招"请求
  response = rpc.request(
    service="BattleService",
    method="cast_ultimate_skill",
    params={"skill_id": "ssr_123", "target": "boss_789"}
  )
  
  # 服务端返回校验结果
  if response["code"] == 0:
    show_skill_animation(response["damage"])
  else:
    show_error("技能释放失败") 
  ```
  - **防作弊机制**：服务端完全掌控伤害计算公式

- **跨服组队匹配**：
  ```go
  // 匹配服务返回队伍信息
  type MatchResult struct {
    TeamID   string
    Members  []PlayerInfo
    DungeonID int
  }
  
  func MatchPlayers(players []PlayerInfo) MatchResult {
    // 通过RPC调用匹配算法微服务
    result := rpc.Call("MatchmakingService.start", players)
    return unmarshal(result) //反序列化
  }
  ```

#### 2.3 ACT游戏（如《怪物猎人：崛起》）
- **实时战斗同步**：
  
  ```c++
  // 同步太刀见切斩动作帧
  struct CombatFrame {
    int64 timestamp;
    Vector3 player_position;
    Quaternion rotation;
    int attack_phase; // 0:准备 1:无敌帧 2:收招
  };
  
  // 每16ms同步一次关键帧
  rpc.Push("CombatSync.pushFrame", current_frame);
  ```
  - **优化技巧**：使用增量编码压缩数据包
  
- **动态难度调整**：
  ```lua
  -- 根据玩家实时表现调整Boss血量
  function adjustBossDifficulty()
    local avg_dps = rpc.call("AnalyticsService.getAvgDPS", party_id)
    local new_hp = calculateDynamicHP(avg_dps)
    rpc.notify("BossAI.setHP", new_hp)
  end
  ```

---

### 三、游戏开发中RPC的独特设计
#### 3.1 通信模式创新
| 模式        | 描述                          | 应用场景                     |
| ----------- | ----------------------------- | ---------------------------- |
| **单向RPC** | 不等待响应（Fire-and-Forget） | 非关键事件（如玩家表情动作） |
| **流式RPC** | 持续双向数据流                | 实时语音聊天、战斗回放同步   |
| **广播RPC** | 一对多通知                    | 全服公告、战场状态更新       |

#### 3.2 性能优化方案
1. **二进制序列化**：Protocol Buffers vs FlatBuffers
   ```protobuf
   // Protobuf定义玩家移动数据
   message PlayerMovement {
     required int32 player_id = 1;
     required Vector3 position = 2;
     optional uint32 timestamp = 3;
   }
   ```
   - **FlatBuffers优势**：零解析开销，直接内存访问

2. **连接复用策略**
   ```text
   TCP连接池管理：
   ┌────────────┐       ┌──────────────┐
   │ GameClient │───▶保持10个长连接───▶│ GameServer  │
   └────────────┘       └──────────────┘
   ```

3. **负载均衡实践**
   ```yaml
   # 基于Consul的服务发现配置
   services:
     - name: "BattleService"
       tags: ["region=us-west", "type=main"]
       health_check: "/health"
       load_balancer: "least_connections"
   ```

---

### 四、行业级解决方案
#### 4.1 腾讯游戏云（TGPC）
- **弹性伸缩架构**：
  ```text
  战斗服扩容流程：
  1. 监控系统检测到负载 > 80%
  2. 调用Kubernetes API扩容Pod
  3. 新实例向Consul注册服务
  4. 负载均衡器自动分流
  ```

#### 4.2 Unity Netcode的RPC实现
```csharp
// Unity中声明网络方法
[ServerRpc]
void RequestRespawnServerRpc(ulong clientId) {
    if(IsServer) RespawnPlayer(clientId);
}

[ClientRpc]
void RespawnClientRpc(Vector3 position) {
    transform.position = position;
}
```

#### 4.3 网易游戏的开源方案
- **Pomelo框架特性**：
  - 基于Node.js的高并发处理
  - 内置AOI（兴趣范围）管理
  - 支持插件式扩展

---

### 五、避坑指南
1. **网络延迟补偿**：
   ```python
   # 客户端预测+服务端校正
   client_position = predict_movement(input)
   server_position = rpc.call("MovementService.sync", client_position)
   if distance(client_position, server_position) > threshold:
       correct_position(server_position)
   ```

2. **反作弊设计**：
   ```java
   // 服务端关键逻辑校验
   public class CombatService {
       @RpcService
       public DamageResult calculateDamage(AttackRequest request) {
           // 1. 验证玩家攻击CD时间
           // 2. 校验装备数值合法性
           // 3. 重新计算伤害值
           return realDamage;
       }

**3.可以使用流量削峰策略**

- 这里先不展开了。

开发者需要根据游戏类型选择适配的RPC策略：比如开放世界注重状态同步，回合制注重逻辑验证,ACT游戏则追求极致实时性。



# 举例

> 以原神释放技能和传送为例，详细写一下客户端RPC的代码逻辑，以及RPC的调用是不是需要写一个回调函数，接收服务器的返回值并在客户端表现逻辑，这个也写一下吧

以下是基于《原神》中 **技能释放** 和 **地图传送** 场景的 RPC 实现代码示例，包含完整的客户端回调处理逻辑。我们将使用 **C# + Unity** 作为示例框架，采用 **异步/回调模式** 实现：

---

### 一、技能释放的完整 RPC 流程（火元素战技为例）

#### 1.1 客户端发起请求
```csharp
// 客户端代码 - SkillController.cs
public class SkillController : MonoBehaviour 
{
    // 引用RPC客户端组件
    private RpcClient _rpcClient; 

    // UI引用
    [SerializeField] private SkillCooldownUI _cooldownUI;

    // 触发火元素战技
    public void CastFireSkill(Vector3 targetPosition)
    {
        // 本地预表现：立即播放动画
        PlayLocalFireAnimation();

        // 构建RPC请求
        var request = new SkillCastRequest {
            SkillId = 101, 
            SourcePlayerId = Player.Local.Id,
            TargetPosition = targetPosition,
            Timestamp = NetworkTime.GetTimestamp()
        };

        // 发起异步RPC调用，注册回调
        _rpcClient.Call<SkillCastResponse>(
            "SkillService.Cast", 
            request,
            OnSkillCastResponse,  // 成功回调
            OnSkillCastError      // 失败回调
        );
    }

    // 本地预表现动画（无需等待服务器）
    private void PlayLocalFireAnimation() {
        GetComponent<Animator>().SetTrigger("FireSkill");
        Instantiate(_fireVfxPrefab, transform.position);
    }

    // RPC成功回调
    private void OnSkillCastResponse(SkillCastResponse response)
    {
        if (response.Success) {
            // 服务器确认后的正式表现
            ApplyDamageNumbers(response.DamageResults);
            UpdateSkillCooldown(response.NewCooldown);
        } else {
            // 服务器拒绝后的回滚
            CancelLocalAnimation();
            ShowErrorMessage(response.ErrorMessage);
        }
    }

    // RPC失败回调（网络问题）
    private void OnSkillCastError(RpcException error) {
        ShowErrorMessage("网络连接失败");
        CancelLocalAnimation();
    }
}
```

#### 1.2 服务器处理逻辑
```csharp
// 服务器代码 - SkillService.cs
public class SkillService : RpcServiceBase
{
    [RpcMethod]
    public SkillCastResponse Cast(SkillCastRequest request)
    {
        // 1. 反作弊校验
        if (!ValidatePlayerPosition(request.SourcePlayerId, request.Timestamp)) {
            return new SkillCastResponse { Success = false, ErrorMessage = "异常位置" };
        }

        // 2. 技能CD校验
        var player = GetPlayer(request.SourcePlayerId);
        if (!player.SkillSystem.IsSkillReady(request.skillId)) {
            return new SkillCastResponse { Success = false, ErrorMessage = "技能冷却中" };
        }

        // 3. 执行技能逻辑
        var damageResults = CalculateDamage(player, request.TargetPosition);
        player.SkillSystem.StartCooldown(request.skillId);

        // 4. 广播给其他客户端（重要！）
        BroadcastToNearbyPlayers(
            new SkillBroadcast {
                SkillId = request.skillId,
                SourceId = request.SourcePlayerId,
                TargetPosition = request.TargetPosition
            }
        );

        return new SkillCastResponse {
            Success = true,
            DamageResults = damageResults,
            NewCooldown = player.SkillSystem.GetCooldown(request.skillId)
        };
    }
}
```

#### 1.3 其他客户端接收广播
```csharp
// 客户端代码 - SkillBroadcastHandler.cs
public class SkillBroadcastHandler : MonoBehaviour 
{
    [RpcListener("SkillBroadcast")] 
    private void OnSkillBroadcast(SkillBroadcast data)
    {
        // 找到释放技能的玩家对象
        var sourcePlayer = FindPlayer(data.SourceId);
        
        // 播放动画和特效（不需要回调）
        sourcePlayer.GetComponent<Animator>().SetTrigger("FireSkill");
        Instantiate(_remoteFireVfxPrefab, data.TargetPosition);

        // 如果目标是自己，显示伤害数字
        if (IsLocalPlayerAffected(data.TargetPosition)) {
            ShowDamageNumbers(data.DamageResults);
        }
    }
}
```



### 二、地图传送的 RPC 实现（带加载过渡）

#### 2.1 客户端发起传送请求
```csharp
// 客户端代码 - TeleportController.cs
public class TeleportController : MonoBehaviour 
{
    [SerializeField] private LoadingScreen _loadingScreen;

    public void RequestTeleport(int waypointId)
    {
        // 显示加载界面
        _loadingScreen.Show("正在传送...");

        // 发起RPC请求
        _rpcClient.Call<TeleportResponse>(
            "WorldService.Teleport",
            new TeleportRequest {
                PlayerId = Player.Local.Id,
                WaypointId = waypointId
            },
            OnTeleportSuccess,
            OnTeleportError
        );
    }

    private void OnTeleportSuccess(TeleportResponse response)
    {
        // 关闭加载界面
        _loadingScreen.Hide();

        // 场景切换分两种情况：
        if (response.IsSameScene) {
            // 同场景传送：直接更新位置
            Player.Local.Teleport(response.NewPosition);
        } else {
            // 跨场景传送：异步加载新场景
            StartCoroutine(LoadNewSceneAsync(response.SceneName, response.NewPosition));
        }
    }

    private IEnumerator LoadNewSceneAsync(string sceneName, Vector3 position)
    {
        var asyncOp = SceneManager.LoadSceneAsync(sceneName);
        while (!asyncOp.isDone) {
            yield return null;
        }
        Player.Local.Teleport(position);
    }

    private void OnTeleportError(RpcException error) {
        _loadingScreen.Hide();
        ShowErrorMessage("传送失败: " + error.Message);
    }
}
```

#### 2.2 服务器验证逻辑
```csharp
// 服务器代码 - WorldService.cs
public class WorldService : RpcServiceBase 
{
    [RpcMethod]
    public TeleportResponse Teleport(TeleportRequest request)
    {
        var player = GetPlayer(request.PlayerId);
        var waypoint = GetWaypoint(request.WaypointId);

        // 1. 校验传送点是否解锁
        if (!player.Progress.IsWaypointUnlocked(waypoint.Id)) {
            throw new RpcException("传送点未解锁");
        }

        // 2. 检查是否在同一场景
        bool isSameScene = (player.Scene == waypoint.Scene);

        // 3. 扣除体力消耗（示例）
        if (!player.TryConsumeStamina(waypoint.StaminaCost)) {
            throw new RpcException("体力不足");
        }

        return new TeleportResponse {
            IsSameScene = isSameScene,
            SceneName = waypoint.Scene,
            NewPosition = waypoint.SpawnPosition
        };
    }
}
```



---

### 三、关键技术解析

#### 3.1 回调的必要性
```csharp
// 异步调用模式示意图
_rpcClient.Call<ResponseType>(
    "Service.Method",   // RPC路径
    requestObject,      // 请求参数
    onSuccess,          // 成功回调（必须）
    onError             // 失败回调（可选）
);

// 为什么要用回调？
// 1. 避免主线程阻塞（网络请求通常需要100ms~1s）
// 2. 允许服务器处理时间不确定
// 3. 方便处理重试逻辑
```

#### 3.2 回调与协程的配合
```csharp
// 使用Unity协程处理多步回调
public IEnumerator TeleportSequence(int waypointId)
{
    var request = new TeleportRequest { /* ... */ };
    
    // 使用TaskCompletionSource桥接回调
    var tcs = new TaskCompletionSource<TeleportResponse>();
    _rpcClient.Call<TeleportResponse>(
        "WorldService.Teleport", 
        request,
        resp => tcs.SetResult(resp),
        err => tcs.SetException(err)
    );

    // 等待异步完成
    yield return tcs.Task;

    // 继续执行后续逻辑
    if (tcs.Task.Result.IsSameScene) {
        // ...
    }
}
```

#### 3.3 错误处理最佳实践
```csharp
// 集中式错误处理器
public class RpcErrorHandler
{
    public static void HandleError(RpcException error)
    {
        switch (error.ErrorCode) {
            case ErrorCode.Timeout:
                ShowToast("请求超时，请检查网络");
                break;
            case ErrorCode.InvalidSession:
                RedirectToLogin();
                break;
            default:
                Log.Error($"RPC错误: {error.Message}");
                break;
        }
    }
}

// 在回调中使用
private void OnTeleportError(RpcException error) {
    RpcErrorHandler.HandleError(error);
    _loadingScreen.Hide();
}
```

---

### 四、高级优化策略

#### 4.1 请求防重发机制
```csharp
// 客户端请求管理器
public class RpcRequestManager : MonoBehaviour
{
    private Dictionary<string, DateTime> _pendingRequests = new();

    public bool TryAddRequest(string requestId) {
        if (_pendingRequests.ContainsKey(requestId)) {
            return false;
        }
        _pendingRequests[requestId] = DateTime.Now;
        return true;
    }

    public void CompleteRequest(string requestId) {
        _pendingRequests.Remove(requestId);
    }
}

// 在技能调用时
var requestId = Guid.NewGuid().ToString();
if (!_requestManager.TryAddRequest(requestId)) return;

_rpcClient.Call("SkillService.Cast", request, 
    resp => {
        _requestManager.CompleteRequest(requestId);
        // ...其他处理
    });
```

#### 4.2 网络延迟补偿
```csharp
// 客户端预测移动代码示例
public void Update() {
    // 本地预测移动
    _predictedPosition += _inputDirection * Time.deltaTime;

    // 每0.2秒同步到服务器
    if (Time.time - _lastSyncTime > 0.2f) {
        SendMovementSync();
    }
}

private void SendMovementSync() {
    _rpcClient.Call("MovementService.Sync", _predictedPosition, 
        resp => {
            // 服务器返回实际位置
            if (Vector3.Distance(_predictedPosition, resp.VerifiedPosition) > 0.5f) {
                // 位置不一致时纠正
                CorrectPosition(resp.VerifiedPosition);
            }
        });
}
```



---

### 五、工程化建议

1. **代码结构组织**
   ```
   /Scripts/Rpc
   ├── Client
   │   ├── Handlers  // RPC回调处理类
   │   └── Services  // 客户端服务代理
   ├── Common
   │   ├── Models    // 数据模型
   │   └── Errors    // 错误类型定义
   └── Server
       └── Services  // 服务端实现
   ```

2. **协议版本管理**
   ```csharp
   // 所有RPC请求携带版本号
   public class RpcRequestBase {
       public string ApiVersion = "1.3.2"; 
   }
   
   // 服务端处理时校验
   if (request.ApiVersion != CurrentApiVersion) {
       throw new RpcException("客户端版本过旧，请更新");
   }
   ```

3. **自动化监控**
   ```csharp
   // 在RPC客户端包装层添加埋点
   public class InstrumentedRpcClient : IRpcClient
   {
       public void Call<T>(string method, object request, Action<T> callback) 
       {
           var stopwatch = Stopwatch.StartNew();
           _innerClient.Call(method, request, resp => {
               stopwatch.Stop();
               Metrics.RecordRpcLatency(method, stopwatch.ElapsedMilliseconds);
               callback(resp);
           });
       }
   }
   ```

---

通过以上实现可以看到，在游戏开发中使用 RPC 的关键在于：

1. **客户端预表现与服务器验证的平衡**：既要保证流畅性，又要防止作弊
2. **完善的错误处理体系**：网络错误、业务错误、版本兼容等
3. **科学的回调管理**：避免内存泄漏，确保生命周期安全
4. **与游戏引擎深度集成**：协程、动画系统、场景管理的无缝衔接

实际项目中还需要结合 **协议压缩**、**流量控制**、**分布式追踪** 等高级技术，才能构建出真正可靠的游戏网络系统。



# Protobuf

### 一、Protobuf 的本质与核心价值

**Protocol Buffers（简称 Protobuf）** 是 Google 开发的跨语言、跨平台、可扩展的 **结构化数据序列化协议**。其核心价值体现在：

1. **二进制编码**：相比 JSON/XML 等文本协议，体积减少 30%-80%
2. **高效编解码**：解析速度比 JSON 快 5-100 倍
3. **强类型约束**：通过 Schema 定义确保数据结构安全
4. **跨语言支持**：自动生成 Java/C#/Python/C++/Go 等代码
5. **版本兼容性**：支持向前向后兼容的协议演进

---

### 二、核心工作原理剖析

#### 2.1 协议定义文件（.proto）
```protobuf
// 定义玩家移动数据协议
syntax = "proto3";

message PlayerMovement {
  int32 player_id = 1;          // 字段编号
  Vector3 position = 2;         // 嵌套消息
  repeated Skill effects = 3;   // 数组类型
  enum State {
    IDLE = 0;
    RUNNING = 1;
  }
  State state = 4;
}

message Vector3 {
  float x = 1;
  float y = 2;
  float z = 3;
}
```

**字段编号规则**：
- 1-15：占用 1 字节存储（常用字段优先使用）
- 16-2047：占用 2 字节
- 不可重复使用
- 已删除字段的编号永久保留

#### 2.2 二进制编码机制
**TLV（Tag-Length-Value）结构**：
```
+-----+---------+-----+---------+-----+---------+
| Tag | Value1 | Tag | Value2 | Tag | Value3 | ...
+-----+---------+-----+---------+-----+---------+
```
- **Tag** = 字段编号 + 数据类型
- **Length** 仅变长类型需要（string/bytes/repeated）
- **Value** 根据数据类型紧凑存储

**编码示例**：
```protobuf
message Test {
  int32 a = 1;
  string b = 2;
}

// 编码数据：a=150, b="testing"
十六进制输出：
08 96 01 12 07 74 65 73 74 69 6e 67
```
- `08` → Tag (字段1, varint类型)
- `96 01` → 150的varint编码
- `12` → Tag (字段2, 长度前缀类型)
- `07` → 字符串长度7
- 后续为"testing"的ASCII码

---

### 三、在游戏开发中的典型应用

#### 3.1 网络协议同步（MOBA游戏示例）
```protobuf
// 战斗帧同步协议
message BattleFrame {
  uint64 frame_id = 1;
  map<int32, PlayerAction> actions = 2;  // 玩家ID到操作的映射
  repeated EntityUpdate entities = 3;    // 实体状态变更
}

message PlayerAction {
  int32 skill_id = 1;
  Vector3 target_pos = 2;
  int64 input_timestamp = 3;  // 用于延迟补偿
}

message EntityUpdate {
  int32 entity_id = 1;
  oneof update_type {          // 联合类型  oneof的介绍：https://blog.csdn.net/whc18858/article/details/131150185，类似于union
    PositionUpdate position = 2;
    HealthUpdate health = 3;
    BuffUpdate buffs = 4;
  }
}
```

**优化效果**：
- 传统JSON：每个帧数据约 2KB
- Protobuf：压缩至 200-500B
- 带宽节省 75% 以上

#### 3.2 游戏存档存储（RPG游戏）
```protobuf
message GameSave {
  uint32 version = 1;
  PlayerData player = 2;
  repeated QuestProgress quests = 3;
  map<int32, Item> inventory = 4;  // 物品槽位映射
  
  message Item {
    int32 item_id = 1;
    int32 count = 2;
    int64 obtain_time = 3;
  }
}

// 二进制存档文件结构：
// [4字节魔数][4字节版本号][Protobuf数据体]
```

**优势体现**：
- 存档加载速度提升 3-5 倍
- 防篡改设计：二进制格式更难直接修改
- 版本升级时自动兼容旧存档

---

### 四、技术实现深度解析

#### 4.1 跨语言代码生成
```bash
# 生成C#代码（Unity使用）
protoc --csharp_out=./output player.proto

# 生成C++代码（UE引擎使用）
protoc --cpp_out=./output player.proto 

# 生成Lua适配器（XLua框架）
protoc --lua_out=./output player.proto
```

**生成代码结构**：
```csharp
// C# 类自动生成
public sealed partial class PlayerMovement : pb::IMessage<PlayerMovement> {
  public int PlayerId { get; set; }
  public Vector3 Position { get; set; }
  private pbc::RepeatedField<Skill> effects_ = new pbc::RepeatedField<Skill>();
  
  public void WriteTo(pb::CodedOutputStream output) {
    if (PlayerId != 0) {
      output.WriteRawTag(8);
      output.WriteInt32(PlayerId);
    }
    // 其他字段序列化...
  }
}
```

#### 4.2 高效序列化流程
```csharp
// Unity中的序列化示例
byte[] SerializeMovement(PlayerMovement move) {
  using (var stream = new MemoryStream()) {
    move.WriteTo(stream);
    return stream.ToArray();
  }
}

PlayerMovement Deserialize(byte[] data) {
  return PlayerMovement.Parser.ParseFrom(data);
}

// 性能对比（10000次操作）：
// JSON: 238ms
// Protobuf: 19ms
```

#### 4.3 版本兼容策略
```protobuf
// 新版本协议扩展
message PlayerData {
  // 保留已删除字段的编号
  reserved 5, 8 to 10;  
  
  // 原有字段
  string name = 1;
  int32 level = 2;
  
  // 新增可选字段
  optional string title = 15;  // 使用大编号
  map<string, int32> achievements = 16;
}

// 旧客户端处理新字段规则：
// - 忽略不识别的字段（兼容性保证）
// - 可选字段自动设为默认值
```

---

### 五、进阶优化技巧

#### 5.1 零拷贝解析（C++示例）
```cpp
// 直接映射内存数据
const GameSave* game_save = flatbuffers::GetRoot<GameSave>(binary_data); 

// 直接访问字段（无解析开销）
int32_t level = game_save->player()->level();
```

#### 5.2 流式处理大型数据
```csharp
// 分块处理角色皮肤数据
using (var input = File.OpenRead("character.bin")) {
  var parser = new MessageParser<Chunk>(() => new Chunk());
  while (true) {
    var chunk = parser.ParseDelimitedFrom(input);
    if (chunk == null) break;
    ProcessChunk(chunk);
  }
}

message Chunk {
  bytes texture_data = 1;  // 1024KB/块
  int32 chunk_index = 2;
}
```

#### 5.3 协议压缩组合
```protobuf
// 组合使用不同编码方案
message OptimizedData {
  oneof compression_type {
    bytes zlib_compressed = 1;  // 常规压缩
    bytes lz4_compressed = 2;   // 快速压缩
    bytes uncompressed = 3;
  }
}
```

---

### 六、行业应用案例

#### 6.1 《原神》网络协议优化
- **挑战**：开放世界动态同步
- **解决方案**：
  - 使用 Protobuf 定义场景实体变更协议
  - 差分编码减少重复数据传输
  - 组合使用 LZ4 压缩二进制流
- **成果**：
  - 移动网络下流量降低 60%
  - 同步延迟稳定在 100ms 以内

#### 6.2 《王者荣耀》战斗回放系统
- **技术方案**：
  ```protobuf
  message ReplayFrame {
    uint32 frame_seq = 1;
    repeated Operation operations = 2;  // 玩家操作记录
    optional Snapshot snapshot = 3;     // 关键帧全量快照
  }
  ```
- **优化点**：
  - 使用 Protobuf 的 optional 标记关键帧
  - 每 60 帧插入一个全量快照
  - 回放文件体积减少 75%

---

### 七、Protocol Buffers v3 重要特性

| 特性          | 说明                  | 游戏开发应用场景         |
| ------------- | --------------------- | ------------------------ |
| **Any 类型**  | 可包装任意类型消息    | 实现灵活的技能效果系统   |
| **Map 类型**  | 原生键值对支持        | 玩家属性表、物品背包数据 |
| **JSON 映射** | 与JSON双向转换        | 方便调试和可视化编辑     |
| **保留字段**  | 防止意外重用字段编号  | 长期维护的多人游戏协议   |
| **选项系统**  | 自定义消息/字段级配置 | 控制不同平台的序列化方式 |

```protobuf
// Any类型使用示例
import "google/protobuf/any.proto";

message SkillEffect {
  string effect_type = 1;
  google.protobuf.Any detail = 2;  // 可以是Damage/Heal/Buff等
}
```

---

### 八、与其他序列化方案对比

| 维度             | Protobuf             | JSON              | FlatBuffers        | MessagePack  |
| ---------------- | -------------------- | ----------------- | ------------------ | ------------ |
| **序列化速度**   | 快（需解析）         | 慢                | **极快（零解析）** | 快           |
| **反序列化速度** | 快                   | 慢                | **极快**           | 快           |
| **数据体积**     | 小                   | 大                | 中等               | 中等         |
| **可读性**       | 需工具               | 好                | 需工具             | 需工具       |
| **模式演进**     | 优秀                 | 无约束            | 良好               | 无约束       |
| **内存占用**     | 低                   | 高                | **极低**           | 低           |
| **适用场景**     | 网络协议、持久化存储 | 配置文件、Web API | 移动端内存敏感场景 | 临时数据传输 |

---

### 九、最佳实践指南

1. **字段编号规划策略**：
   - 1-15：高频基础字段（位置、状态）
   - 16-2047：扩展字段
   - 预留 1000 个编号给未来扩展

2. **版本兼容性设计**：
   ```protobuf
   // V1.0
   message Player {
     int32 id = 1;
     string name = 2;
   }
   
   // V2.0
   message Player {
     int32 id = 1;
     string name = 2;
     optional string nickname = 15;  // 新增可选字段
     reserved 3;                     // 标记已删除字段
   }
   ```

3. **性能敏感场景优化**：
   ```csharp
   // 复用解析器实例（避免重复创建）
   private static readonly MessageParser<PlayerMove> _parser 
       = new MessageParser<PlayerMove>(() => new PlayerMove());
   
   public PlayerMove Parse(byte[] data) {
       return _parser.ParseFrom(data);
   }
   ```

4. **安全防护方案**：
   ```protobuf
   // 设置消息大小限制
   message Config {
     option (message_max_size) = 102400;  // 最大100KB
     // ...
   }
   ```

---

通过深入使用 Protobuf，游戏开发者可以获得：
- **网络带宽利用率提升**：更小的数据包体积
- **CPU消耗降低**：更高效的编解码性能
- **跨平台一致性保障**：自动生成的严格类型约束
- **长期可维护性**：优雅的协议演进能力

建议将 Protobuf 与 gRPC 框架结合，构建完整的游戏网络通信体系，同时配合性能分析工具（如 Perfetto）持续优化关键路径。



### 测试

这个网站可以测试Protobuf转各种语言的脚本：[Protobuf Code Generator and Parser | protobufnet | Marc Gravell](https://protogen.marcgravell.com/)

测试用例可以去这个博客复制：[Protobuf 的简单使用例子_protocobuf的例子-CSDN博客](https://blog.csdn.net/m0_45867846/article/details/114603744)

看完上文之后，可以看一下Protobuf在Unity当中的使用技巧：[手把手教你如何在Unity中使用Google.Protobuf3(一) Protobuf.dll获取获取_unity 接入proto3报错-CSDN博客](https://blog.csdn.net/qq_42461824/article/details/116734000)



# RPC与属性同步

比如以下的一些业务场景，可能的同步方案分别如下：

#### （a）一些业务场景举例

> 以下是针对四个业务场景的同步方案设计，基于属性同步与RPC的适用场景对比：
>
> ---
>
> ### **1. 《原神》深渊副本战斗同步**  
>
> | **同步内容**     | **方案** | **属性同步设计**                            | **RPC设计**                                       |
> | ---------------- | -------- | ------------------------------------------- | ------------------------------------------------- |
> | **角色移动**     | 属性同步 | `位置`、`旋转`（高频低精度同步，优化阈值）  | 无                                                |
> | **技能释放**     | RPC      | 无                                          | `ServerRPC_RequestCastSkill`（客户端→服务器请求） |
> | **受击伤害计算** | RPC      | 无                                          | `ServerRPC_ApplyDamage`（服务器权威计算）         |
> | **受击特效**     | RPC      | 无                                          | `ClientRPC_PlayHitEffect`（服务器→客户端广播）    |
> | **角色血量**     | 属性同步 | `Health`（服务器同步至客户端）              | 无                                                |
> | **技能冷却时间** | 属性同步 | `SkillCooldown`（仅同步剩余时间，低频更新） | 无                                                |
> | **副本计时器**   | 混合     | `RemainingTime`（服务器同步至客户端）       | `ClientRPC_OnTimerEnd`（计时结束时触发事件）      |
>
> **计时器逻辑**：  
>
> - **服务器权威计时**：服务器维护剩余时间并同步至客户端（避免客户端篡改）。  
> - **完成事件触发**：通过RPC通知客户端播放结束动画或结算界面。
>
> ---
>
> ### **2. 回合制游戏（手动 vs 自动战斗）**  
>
> | **战斗模式** | **同步策略** | **属性同步设计**                        | **RPC设计**                                      |
> | ------------ | ------------ | --------------------------------------- | ------------------------------------------------ |
> | **手动战斗** | RPC为主      | `CurrentTurnPlayer`（当前回合玩家ID）   | `ServerRPC_SelectAction`（玩家操作提交至服务器） |
> |              |              | `BattleState`（战斗阶段：准备/执行）    | `ClientRPC_ExecuteAction`（服务器广播执行结果）  |
> | **自动战斗** | 属性同步为主 | `AutoActionQueue`（服务器生成行动队列） | `ClientRPC_OnAutoComplete`（自动流程结束时通知） |
> |              |              | `BattleResult`（战斗结果同步）          | 无                                               |
>
> **关键区别**：  
>
> - **手动战斗**：依赖RPC提交玩家操作，服务器验证后同步结果。  
> - **自动战斗**：服务器直接计算并同步行动队列和结果（减少RPC交互）。
>
> ---
>
> ### **3. 俄罗斯方块小活动同步**  
>
> | **同步内容**     | **方案** | **属性同步设计**                           | **RPC设计**                            |
> | ---------------- | -------- | ------------------------------------------ | -------------------------------------- |
> | **当前方块状态** | 属性同步 | `CurrentBlockType`、`Position`（低频同步） | 无                                     |
> | **已堆积方块**   | 属性同步 | `GridData`（二维数组，仅同步变化部分）     | 无                                     |
> | **消除行事件**   | RPC      | 无                                         | `ClientRPC_ClearLines`（播放消除特效） |
> | **玩家得分**     | 属性同步 | `Score`（服务器同步至客户端）              | 无                                     |
> | **游戏状态**     | 属性同步 | `IsGameOver`（同步结束标志）               | `ClientRPC_OnGameOver`（触发结算界面） |
>
> **优化策略**：  
>
> - **延迟补偿**：客户端预测方块下落，服务器校正最终位置。  
> - **数据压缩**：`GridData`使用位掩码（Bitmask）减少带宽。
>
> ---
>
> ### **4. 动作游戏怪物技能同步**  
>
> | **同步内容**       | **方案**   | **属性同步设计**                             | **RPC设计**                                    |
> | ------------------ | ---------- | -------------------------------------------- | ---------------------------------------------- |
> | **怪物位置/朝向**  | 属性同步   | `Position`、`Rotation`（服务器同步至客户端） | 无                                             |
> | **技能释放事件**   | RPC        | 无                                           | `MulticastRPC_StartSkill`（广播技能起手动作）  |
> | **抛物线子弹轨迹** | 确定性计算 | 无（客户端根据公式计算轨迹）                 | `ServerRPC_SpawnBullet`（服务器生成子弹参数）  |
> | **子弹命中判定**   | 服务器权威 | 无                                           | `ServerRPC_CheckHit`（客户端提交命中检测请求） |
> | **怪物血量**       | 属性同步   | `Health`（服务器同步至客户端）               | 无                                             |
>
> **抛物线子弹同步方案**：  
>
> 1. **参数同步**：服务器通过RPC广播子弹的起点、初速度、重力参数。  
> 2. **客户端计算**：所有客户端根据相同公式（如 `位置=起点+速度*t + 0.5*重力*t²`）实时计算轨迹，避免逐帧同步位置。  
> 3. **服务器验证**：客户端提交命中检测请求，服务器权威判定是否有效。
>
> ---
>
> ### **总结**  
>
> - **属性同步**：用于**持续、高频、数值型数据**（位置、血量、状态）。  
> - **RPC**：用于**离散事件、逻辑触发**（技能释放、特效播放）。  
> - **混合策略**：复杂场景需结合两者（如计时器同步数值+事件触发）。

因此，在选择属性同步或RPC时，需要考虑以下问题：

- 你是否真的需要关注每次值的变化，还是只需要最新值来完成某些操作；
- 以及这个数据是否可以接受可能会丢失的情况，因为不可靠的RPC可能会丢包。属性同步综合来说是可靠的（虽迟但到）。

当然，你也可以使用可靠的RPC调用来保证数据一定会到达，但显然开销会增加。因此，一般来说，**RPC应用于效果提示和类似的非关键网络信息传递，而属性同步则用于其他一切。**无论如何，属性同步都会在Actor身上发生。**如果你真的只需要触发一个一次性事件，而且你不在乎该事件是否会被丢弃，或者你需要从客户端向服务器发送数据，那么使用RPC是合适的。**



### 一些知识点补充

> ### **1. 属性同步是否主要用于“状态同步”类游戏？**  
> **答**：属性同步是**所有实时多人在线游戏的基础机制**，并非仅限于特定类型。其核心目标是保证所有客户端与服务器的**状态一致性**，适用于任何需要共享动态数据的场景：  
>
> | **游戏类型**   | **属性同步的应用**                       | **必要性**               |
> | -------------- | ---------------------------------------- | ------------------------ |
> | **原神**       | 同步角色位置、血量、技能冷却、任务进度   | 必需（基础状态一致性）   |
> | **回合制游戏** | 同步回合状态、自动战斗队列、战斗结果     | 必需（减少RPC交互频率）  |
> | **动作游戏**   | 同步怪物位置、玩家受击状态、子弹轨迹参数 | 必需（避免预测误差累积） |
> | **休闲小游戏** | 同步俄罗斯方块网格、得分、游戏结束状态   | 必需（低带宽高效同步）   |
>
> **结论**：只要涉及多玩家实时交互，属性同步都是必选方案，与游戏类型无关。
>
> ---
>
> ### **2. 哪些RPC需要可靠（Reliable）？哪些可以不可靠（Unreliable）？**  
> RPC的可靠性选择取决于**业务逻辑的严格性**和**数据丢失的容忍度**，关键原则如下：  
>
> #### **可靠RPC（Reliable）适用场景**  
> | **场景**             | **原因**                                             | **示例**                                           |
> | -------------------- | ---------------------------------------------------- | -------------------------------------------------- |
> | **技能释放请求**     | 客户端请求必须到达服务器，否则技能无法触发           | `ServerRPC_Attack`（客户端→服务器，需保证执行）    |
> | **伤害计算结果同步** | 服务器计算的伤害必须广播到客户端，避免玩家血量不同步 | `ClientRPC_ApplyDamage`（服务器→客户端，不可丢失） |
> | **游戏关键事件**     | 游戏开始/结束、回合切换等事件必须可靠触发            | `MulticastRPC_StartGame`（服务器→所有客户端）      |
>
> #### **不可靠RPC（Unreliable）适用场景**  
> | **场景**         | **原因**                                       | **示例**                                                     |
> | ---------------- | ---------------------------------------------- | ------------------------------------------------------------ |
> | **特效播放**     | 偶尔丢失不影响游戏逻辑，如爆炸特效可允许丢包   | `MulticastRPC_PlayExplosion`（服务器→客户端，允许部分丢失）  |
> | **高频位置更新** | 位置同步本身会被后续数据覆盖，丢失个别包无影响 | `ClientRPC_UpdatePosition`（服务器→客户端，用于非权威对象的辅助同步） |
> | **语音聊天**     | 实时语音可容忍短暂中断，优先低延迟             | `ClientRPC_TransmitVoice`（客户端→客户端，通过服务器转发）   |
>
> ---
>
> ### **3. 释放技能是否需要可靠RPC？爆炸特效是否可不可靠？**  
> - **技能释放**：**必须可靠**。  
>   - 若客户端释放技能的RPC丢失，服务器不会执行逻辑，导致玩家按下技能但无效果，破坏体验。  
>   - **引擎实现**：  
>     - **UE**：`UFUNCTION(Server, Reliable)`  
>     - **Unity**：`[ServerRpc(Delivery = RpcDelivery.Reliable)]`  
>
> - **爆炸特效**：**通常不可靠**。  
>   - 若特效播放的RPC丢失，客户端可能看不到一次爆炸，但游戏逻辑不受影响（伤害已通过可靠RPC计算）。  
>   - **例外**：若特效与逻辑强关联（如炸弹爆炸后生成可拾取道具），则需可靠RPC。  
>
> ---
>
> ### **4. 可靠性配置的通用规则**  
> | **维度**           | **可靠RPC**                    | **不可靠RPC**                |
> | ------------------ | ------------------------------ | ---------------------------- |
> | **数据重要性**     | 影响核心逻辑（伤害、状态切换） | 仅影响表现层（特效、音效）   |
> | **触发频率**       | 低频（每次操作需精确到达）     | 高频（数据可被后续更新覆盖） |
> | **延迟容忍度**     | 允许稍高延迟（确保到达）       | 要求低延迟（允许丢包）       |
> | **典型网络层协议** | TCP或Reliable UDP              | Unreliable UDP               |
>
> ---
>
> ### **5. 为什么不可靠RPC仍被广泛使用？**  
> - **带宽优化**：避免因重传导致带宽浪费（如UE的 `NetMulticast` 默认不可靠）。  
> - **实时性优先**：动作游戏中角色移动同步更关注实时性而非绝对可靠（后续数据覆盖之前状态）。  
> - **容错设计**：客户端可预测或插值补偿丢失的RPC（如爆炸特效客户端本地预测播放）。  
>
> ---
>
> ### **总结**  
> - **属性同步**是游戏网络同步的基石，与游戏类型无关。  
> - **RPC可靠性**需根据业务逻辑选择：  
>   - **可靠RPC**：用于技能、伤害、状态切换等关键逻辑。  
>   - **不可靠RPC**：用于特效、音效、高频位置更新等表现层需求。  
> - **设计建议**：在UE/Unity中明确标记RPC可靠性（如 `Reliable` 或 `Unreliable`），避免混淆。
