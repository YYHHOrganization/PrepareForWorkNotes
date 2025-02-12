# Unity物理引擎碰撞检测说明



# 一、OnTriggerEnter和OnCollisionEnter的调用要求

### 1. OnTriggerEnter与OnCollisionEnter的调用时机及组件关系

### （1）OnCollisionEnter

- **调用条件**：

  - OnCollisionEnter：当两个物体发生物理碰撞时触发，双方均需满足: Collider的isTrigger=false
    - 至少一个物体有 **Rigidbody**（非Kinematic），并且碰撞的主动方需要有Rigidbody。如果双方都有Rigidbody且一方为Kinematic，则Kinematic的一方在碰撞时不会发生动力学模拟。

  比如下面这个例子：

  ![image-20250210190528530](Unity%E7%89%A9%E7%90%86%E5%BC%95%E6%93%8E%E7%A2%B0%E6%92%9E%E6%A3%80%E6%B5%8B%E8%AF%B4%E6%98%8E.assets/image-20250210190528530.png)

  A和B身上都挂了一个带有OnCollisionEnter回调函数的脚本，测试以下情况（如无特殊说明不会勾选isKinematic和isTrigger）：

  - （1）A和B都有Collider但无Rigidbody，此时都不调用；

  - （2）A和B两者都有Rigidbody，此时A撞B或者B撞A，两者身上的OnCollisionEnter都会回调；
  - （3）A有Rigidbody，B没有Rigidbody，此时用A去撞B，两者身上的OnCollisionEnter都会回调；但注意，如果用B去撞A，则不一定会及时调用OnCollisionEnter，这是因为**物理响应的方向**：没有Rigidbody的物体（B）无法主动触发碰撞事件，需由带有非kinematic（运动学）刚体的物体（A）主动移动或受力才能触发。
    - **也就是说，碰撞的主动方需要是刚体Rigidbody。**
  - （4）A和B至少有一个设置成了isTrigger，此时有rigidbody也不会发生OnCollisionEnter的回调；
  - （5）A和B都有Rigidbody并且都设置成了isKinematic，此时不会发生OnCollisionEnter回调；
  - （6）A和B都有Rigidbody，但A设置成了isKinematic，B没有，此时A去撞B或者用B去撞A，两者都会发生OnCollisionEnter回调，但A不会发生动力学模拟（意味着拿A来回扫B或者拿B来回扫A是会触发碰撞回调的，B可能会飞上天，但A岿然不动）；

  

  ### （2）OnTriggerEnter

  - OnTriggerEnter：当物体穿透另一个物体时触发，触发条件为：
    - 至少一方勾选Collider的 **isTrigger=true**，且至少一方有 Rigidbody（可设置为Kinematic）。
    - 与OnCollisionEnter相比，至少一方得是isTrigger，至少一方得有Rigidbody，但对Kinematic没有要求。

  测试以下的情况（没有特殊说明都没有勾选isTrigger和isKinematic）：

  - （1）A和B都有Collider，但都没有Rigidbody，此时两者OnTriggerEnter无论如何都不会回调；
  - （2）A有Rigidbody，同时是isTrigger；B没有Rigidbody：此时B撞A或者A撞B都会回调两者的OnTriggerEnter（B有没有勾选isTrigger都会回调的）；
  - （3）A没有Rigidbody，但是是isTrigger；B有Rigidbody：此时B撞A或者A撞B依旧都会回调两者的OnTriggerEnter（B有没有勾选isTrigger都会回调）；
  - （4）任意一方勾选isKinematic都不会影响双方OnTriggerEnter的回调，当然双方都勾选了isKinematic也不影响回调。

  

- 注：关于**组件依赖**：

  - Trigger/Collision检测需双方均有 **Collider**，Rigidbody决定是否参与物理模拟（如重力、受力），但如果想要有Collision或者Trigger则要求至少一方得有Rigidbody（Collision的话发生碰撞的主动方至少得有Rigidbody）
  - 对于Collision来说，至少有一个物体得不是kinematic，勾选isKinematic的对象不会发生动力学模拟；



# 二、实际场景

## 1.子弹命中敌人

- **推荐方案**：
  - **子弹挂载脚本**：若子弹主动移动（如通过Rigidbody或代码控制），将`OnTriggerEnter`/`OnCollisionEnter`写在子弹上，检测到敌人时触发伤害逻辑（如`Enemy.TakeDamage()`），并销毁自身
  - **敌人挂载脚本**：若敌人需响应多种攻击来源（如子弹、近战），可在敌人脚本中统一处理碰撞事件，但需过滤碰撞对象的Tag或Layer
- **选择依据**：
  - 若子弹需要精确控制碰撞逻辑（如不同子弹类型），优先在子弹上写代码
  - 若敌人需统一管理伤害，可在敌人上处理（需确保子弹有Rigidbody和Collider），如果用Collision来做的话因为子弹是碰撞的主动方，需要有Rigidbody。

- **子弹碰撞逻辑最终推荐**：如果用OnTriggerEnter来做的话，优先在子弹上挂载脚本，使用`OnTriggerEnter`（需勾选isTrigger）检测敌人并触发伤害
  - 此时测试A充当子弹，B充当敌人，A勾选isTrigger，挂载Rigidbody；B不勾选isTrigger，挂载Rigidbody。双方都勾选isKinematic，子弹打中敌人时会回调双方的OnTriggerEnter。（敌人主动往子弹上撞也会触发双方的OnTriggerEnter）

> 思考一下绝区零的子弹，其实没有碰撞的动力学模拟，因此设置为Trigger是没什么问题的。敌人的话可能会有别的逻辑，不设置trigger+勾选kinematic是可以的；



## 2.玩家释放技能打中敌人

在Unity中，**玩家技能击中敌人的逻辑推荐使用触发器（Trigger）实现**，**使用触发器的原因**：

- **触发器（`Is Trigger`）适合非物理碰撞的命中检测**，技能通常不需要物理阻挡效果（如弹开敌人），只需检测接触事件即可
- 若使用普通碰撞器（未勾选`Is Trigger`），双方需至少得有一个非Kinematic刚体，否则无法触发`OnCollisionEnter`。而技能可能需快速移动或瞬发，更适合触发器。

具体实现如下：

- （1）**技能碰撞体设置**：在玩家武器的碰撞体上勾选`Is Trigger`，并附加刚体（`Rigidbody`），设置`isKinematic = true`以避免受物理力影响；
- （2）**敌人碰撞体设置**：敌人需有普通碰撞体（不勾选`Is Trigger`），附加刚体（可设为Kinematic或Dynamic）
- （3）**脚本逻辑**：在武器脚本中通过`OnTriggerEnter`检测敌人标签（如`Enemy`），触发伤害计算：

```c#
void OnTriggerEnter(Collider other) {
    if (other.CompareTag("Enemy")) {
        other.GetComponent<EnemyHealth>().TakeDamage(damage);
        SpawnSlashEffect(other.ClosestPoint(transform.position)); // 在接触点生成划痕
    }
}
```

注：若敌人是Kinematic刚体，需确保其碰撞体未勾选`Is Trigger`，否则无法触发武器的`OnTriggerEnter`。技能碰撞体的刚体设为Kinematic可避免物理干扰，但仍能触发检测。



# 三、其他

## 1.关于CharacterController的特殊性

可以参考：[Unity两个物体发生碰撞的条件_unity oncontrollercolliderhit-CSDN博客](https://blog.csdn.net/qiaoquan3/article/details/51339373)，但也不准确，**这东西Unity搞得属实是有点逆天。**

> 个人经验：角色CharacterController，还要额外挂一个Trigger，用于一些机关什么的检测玩家进入，比如电梯。**参考文献不用看，没有全对的。**

**CharacterController** 是专为角色移动设计的组件，自带胶囊体Collider，无需Rigidbody即可移动和碰撞检测。

注：**Rigidbody** 用于物理模拟（如受外力、重力），与CharacterController功能冲突，一般不同时使用。

- **注意事项**：
  - **移动方式**：必须通过 `Move()` 方法控制移动，而非直接修改Transform。
  - **碰撞检测**：使用 `OnControllerColliderHit()` 而非 `OnCollisionEnter`
  - **推动物体**：若需推动其他物体（如箱子），需在 `OnControllerColliderHit()` 中手动为对方添加力
  - **穿透问题**：高速度移动时可能穿透薄Collider，可通过`Min Move Distance`或射线检测提前修正

| 目标事件                  | 条件                                                         |
| ------------------------- | ------------------------------------------------------------ |
| `OnControllerColliderHit` | CharacterController通过`Move()`碰撞到其他非触发器物体时触发  |
| 对方的`OnCollisionEnter`  | 对方需有**刚体**且**未勾选Is Trigger**，且由CharacterController主动移动碰撞时触发（对方） |
| 对方的`OnTriggerEnter`    | 对方需**勾选Is Trigger**（有无刚体均可），CharacterController接触时触发 |

注：CharacterController的 `OnControllerColliderHit` 适用于非Trigger碰撞（如推箱子），而触发伤害需依赖Trigger机制（比如敌人拿刀击中玩家，造成伤害）。



注2：

- （1）假如A,B都是CharacterController：B不动，A移动去碰B，只有A会获得回调。（**未验证**）

- （2）假如Player是ChacterController，B是Collision（没有勾选isTrigger），B没有刚体的情况下：

  - 1.Player移动去碰B（只有调用`Move`的时候），则Player有消息回调OnControllerColliderHit（B中的OnCollisionEnter不会被回调）,并且B不动，A会走CharacterController的策略（比如说爬楼梯、蹭过去），**常见业务场景应该就是玩家撞到场景物体。**
  - 2.B去碰Player，Player会被挤开，B不动，但是**不会触发任何消息回调**。
    - Player身上的回调，B的回调都没有。

- 如果B有刚体，并且没有勾选isKinematic的情况下：

  - Player 通过Move方法去碰B，A只有OnControllerColliderHit回调，B没有回调，B不动，A不会弹开（但是会走CharacterController的表现逻辑）；
  - B去碰Player：Player、B都只能收到OnCollisionEnter回调（Player收不到`OnControllerColliderHit`）。

  - 4.如果B有刚体，且B勾选isKinematic的情况（**这种情况和B没有刚体是一样的**）：
    - Player 通过Move方法去碰B：B没有动（因为B是Kinematic）,Player走CharacterController的表现逻辑，只有`OnControllerColliderHit`会回调。
    - B去碰Player：B没有动（因为B是Kinematic），Player走CharacterController的表现逻辑（会被推开）。**双方没有任何回调。**

- （3）假如Player是ChacterController，B是Trigger（B有没有rigidbody不影响，是不是isKinematic也不影响）。
  - B碰Player会触发B的OnTriggerEnter回调（也会触发Player的OnTriggerEnter回调）
  - Player碰B也会触发双方的OnTriggerEnter回调（**诡异的是Player走上B不会触发OnTriggerEnter回调，但是侧身蹭到B会触发B的OnTriggerEnter回调**）

可以使用以下这两张图辅助记忆！

![image-20250210235105727](Unity%E7%89%A9%E7%90%86%E5%BC%95%E6%93%8E%E7%A2%B0%E6%92%9E%E6%A3%80%E6%B5%8B%E8%AF%B4%E6%98%8E.assets/image-20250210235105727.png)



关于Trigger的情况：

![image-20250210235705050](Unity%E7%89%A9%E7%90%86%E5%BC%95%E6%93%8E%E7%A2%B0%E6%92%9E%E6%A3%80%E6%B5%8B%E8%AF%B4%E6%98%8E.assets/image-20250210235705050.png)



### （1）敌人武器击中玩家的写法

#### **1. 玩家配置**

- **添加Trigger Collider**
  在玩家物体上添加一个 **Collider**（如Capsule或Box Collider），并勾选 **Is Trigger**。此Collider负责检测敌人武器的攻击范围[1](https://gwb.tencent.com/community/detail/133440)[4](https://www.zhihu.com/question/7826983338/answer/64459890454)。

- **挂载脚本处理伤害**
  在玩家脚本中实现 `OnTriggerEnter` 方法，检测是否与敌人武器接触：

  ```
  csharp复制代码void OnTriggerEnter(Collider other) 
  {
      if (other.CompareTag("EnemyWeapon")) 
      {
          // 减少玩家血量
          TakeDamage();
      }
  }
  ```

------

#### **2. 敌人武器配置**

- **添加Trigger Collider**
  在武器上添加一个 **Collider**（根据武器形状选择类型），并勾选 **Is Trigger**。确保其大小覆盖攻击范围[1](https://gwb.tencent.com/community/detail/133440)[5](https://www.nowcoder.com/discuss/601045247090565120)。
- **附加Rigidbody（可选）**
  若武器需要物理运动（如被击飞），可添加 **Rigidbody** 并勾选 **Is Kinematic**，避免物理引擎干扰武器运动[6](https://www.cnblogs.com/willbin/p/3414017.html)[9](https://blog.51cto.com/u_12207/10788032)。
- **设置Tag或Layer**
  为武器物体设置唯一标签（如 `EnemyWeapon`），或在代码中通过Layer过滤碰撞[5](https://www.nowcoder.com/discuss/601045247090565120)。

------

#### **3. 为何不使用OnControllerColliderHit？**

- **触发条件限制**
  `OnControllerColliderHit` 仅在 **CharacterController主动移动并碰撞非Trigger物体时触发**。若敌人武器是Trigger或由其他方式移动（如动画），此方法不会触发[1](https://gwb.tencent.com/community/detail/133440)[10](https://blog.csdn.net/weixin_41697242/article/details/121715393)。
- **双向检测问题**
  与CharacterController碰撞时，如果敌人的刀是主动移动的一方，只有主动移动的一方（如敌人）会收到回调，被动方（玩家）无事件响应[1](https://gwb.tencent.com/community/detail/133440)[4](https://www.zhihu.com/question/7826983338/answer/64459890454)。当然如果敌人是Trigger的话敌人撞到玩家会调用双方的OnTriggerEnter方法。



## 2.关于角色上电梯不抖的问题

假设角色使用的是CharacterController，减少抖动的方法如下（经过测试）：

- （1）电梯设置为Collider（不是Trigger，但是可以额外加一个Trigger判断玩家是否在电梯里），用来拖住玩家。电梯不需要是Rigidbody。
- （2）玩家就是正常的CharacterController，不需要加额外的组件；
- （3）电梯开始移动的逻辑：既可以是Player的`OnControllerColliderHit`回调，也可以通过电梯额外加的的Trigger回调（感觉会更好）
- （4）**重点：电梯移动的时候同步一个externalMove给玩家，用于在Move的时候额外加Y轴的偏移。**

> 缺点：电梯上无法跳跃，会被禁用掉。

测试用例需要的脚本：

```c#
//player身上的，重点看Update函数
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Serialization;

public class TestControllerCollision : MonoBehaviour
{
    private void OnControllerColliderHit(ControllerColliderHit hit)
    {
        if (hit.gameObject.CompareTag("testPhysics"))
        {
            Debug.Log("OnControllerColliderHit " + hit.gameObject.name);
        }

        if (hit.gameObject.CompareTag("InteractiveObject")) //可交互物体
        {
            hit.gameObject.GetComponent<IInteractiveItem>().Do(this.gameObject);
        }
        
    }
    
    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("testPhysics"))
        {
            Debug.Log("OnTriggerEnter " + other.gameObject.name);
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("testPhysics"))
        {
            Debug.Log("Player OnCollisionEnter " + collision.gameObject.name);
        }
    }

    private CharacterController controller;
    private Vector3 playerVelocity;
    private bool groundedPlayer;
    private float playerSpeed = 5.0f;
    private float jumpHeight = 1.0f;
    private float gravityValue = -9.81f;
    
    private Vector3 externalMove = Vector3.zero;
    
    private void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    private Vector3 curMoveMotion;
    public Vector3 CurMoveMotion
    {
        get { return curMoveMotion; }
    }
    
    
    private bool confirmOnGround = false;
    public bool ConfirmOnGround
    {
        get { return confirmOnGround; }
        set { confirmOnGround = value; }
    }
    

    private void Update()
    {
        groundedPlayer = controller.isGrounded;
        //Debug.Log("isGrounded: " + groundedPlayer); //在电梯上是false
        if (groundedPlayer && playerVelocity.y < 0)
        {
            playerVelocity.y = 0f;
        }

        Vector3 move = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
        controller.Move(move * Time.deltaTime * playerSpeed);

        if (move != Vector3.zero)
        {
            gameObject.transform.forward = move;
        }

        // Makes the player jump
        if (Input.GetButtonDown("Jump") && groundedPlayer)
        {
            playerVelocity.y += Mathf.Sqrt(jumpHeight * -2.0f * gravityValue);
        }

        playerVelocity.y += gravityValue * Time.deltaTime;
        if (externalMove.y != 0) playerVelocity.y = 0; //暂时的做法是,如果有外部移动,则不受重力影响,但是这样会导致角色跳跃不起来(原神中跳跃应该是通过动画实现的?不知是否为Root Motion,感觉先这样就可以了,电梯上不能跳跃)
        //考虑externalMove
        controller.Move((playerVelocity+externalMove) * Time.deltaTime);
        externalMove = Vector3.zero;
    }
    
    public void AddExternalMove(Vector3 externalMove)
    {
        this.externalMove = externalMove;
    }
}

```

另一个脚本是电梯的：

```c#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ElevatorMove : MonoBehaviour, IInteractiveItem
{
    // 1. 电梯的移动速度
    public float speed = 1.0f;
    // 2. 电梯的移动距离
    public float distance = 10.0f;
    // 3. 电梯的移动方向
    public Vector3 direction = Vector3.up;
    private TestControllerCollision playerController;

    private bool moveUp = true;

    //玩家进入Trigger后电梯开始移动
    private bool isMove = false;
    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Player")) //如果走上电梯检测不到,很可能是skin width太大
        {
            Debug.Log("Elevator OnTriggerEnter");
            Do(other.gameObject);
        }
    }

    public void Do(GameObject other)
    {
        Debug.Log("Do!!");
        if(isMove) return;
        isMove = true;
        Debug.Log("Elevator OnCollisionStay");
        playerController = other.GetComponentInParent<TestControllerCollision>();
        StartCoroutine(MoveElevator());
    }

    //电梯移动
    private IEnumerator MoveElevator()
    {
        yield return new WaitForSeconds(2f);
        float moveDistance = 0;
        int upOrDown = moveUp ? 1 : -1;
        while (moveDistance < distance)
        {
            transform.Translate(direction * upOrDown * speed * Time.deltaTime);
            
            if (playerController != null)
            {
                playerController.AddExternalMove(direction * upOrDown * speed); //重点看这句，传入一个ExternalMove给Player
            }
            moveDistance += speed * Time.deltaTime;
            yield return null;
        }

        yield return new WaitForSeconds(1f);
        isMove = false;
        moveUp = !moveUp;
    }
}
```

