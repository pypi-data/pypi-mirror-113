# -*- coding: utf-8 -*-

from mod.server.component.effectCompServer import EffectComponentServer
from mod.server.component.actorMotionCompServer import ActorMotionComponentServer
from mod.server.component.blockInfoCompServer import BlockInfoComponentServer
from mod.client.component.itemCompClient import ItemCompClient
from typing import Union
from mod.client.component.skyRenderCompClient import SkyRenderCompClient
from mod.server.component.rotCompServer import RotComponentServer
from mod.server.component.blockCompServer import BlockCompServer
from mod.server.component.scaleCompServer import ScaleComponentServer
from mod.server.component.gravityCompServer import GravityComponentServer
from mod.server.component.itemCompServer import ItemCompServer
from mod.client.component.virtualWorldCompClient import VirtualWorldCompClient
from typing import Tuple
from mod.client.component.frameAniControlComp import FrameAniControlComp
from mod.client.component.actorMotionCompClient import ActorMotionComponentClient
from mod.client.component.frameAniSkeletonBindComp import FrameAniSkeletonBindComp
from mod.server.component.blockEntityExDataCompServer import BlockEntityExDataCompServer
from mod.client.component.posCompClient import PosComponentClient
from mod.server.component.msgCompServer import MsgComponentServer
from mod.server.component.posCompServer import PosComponentServer
import mod.common.minecraftEnum as minecraftEnum
from mod.server.component.expCompServer import ExpComponentServer
from mod.server.component.flyCompServer import FlyComponentServer
from mod.server.component.nameCompServer import NameComponentServer
from mod.server.component.bulletAttributesCompServer import BulletAttributesComponentServer
from mod.server.component.dimensionCompServer import DimensionCompServer
from mod.client.component.blockUseEventWhiteListCompClient import BlockUseEventWhiteListComponentClient
from mod.server.component.mobSpawnCompServer import MobSpawnComponentServer
from mod.client.component.particleTransComp import ParticleTransComp
from mod.server.component.levelCompServer import LevelComponentServer
from mod.server.component.weatherCompServer import WeatherComponentServer
from Preset.Model.TransformObject import TransformObject
from mod.client.component.auxValueCompClient import AuxValueComponentClient
from mod.client.component.textBoardCompClient import TextBoardComponentClient
from mod.server.component.chunkSourceComp import ChunkSourceCompServer
from mod.server.component.chestContainerCompServer import ChestContainerCompServer
from mod.server.component.tameCompServer import TameComponentServer
from mod.server.component.petCompServer import PetComponentServer
from mod.server.component.engineTypeCompServer import EngineTypeComponentServer
from mod.client.component.textNotifyCompClient import TextNotifyComponet
from mod.server.component.collisionBoxCompServer import CollisionBoxComponentServer
from mod.server.component.biomeCompServer import BiomeCompServer
from mod.client.component.particleSkeletonBindComp import ParticleSkeletonBindComp
from mod.server.component.modelCompServer import ModelComponentServer
from mod.common.utils.timer import CallLater
from mod.client.component.actorRenderCompClient import ActorRenderCompClient
from typing import Any
from mod.server.component.gameCompServer import GameComponentServer
from mod.client.component.frameAniTransComp import FrameAniTransComp
from mod.server.component.rideCompServer import RideCompServer
from mod.client.component.cameraCompClient import CameraComponentClient
from mod.client.component.frameAniEntityBindComp import FrameAniEntityBindComp
from mod.client.component.attrCompClient import AttrCompClient
from mod.server.component.actorPushableCompServer import ActorPushableCompServer
from mod.client.component.recipeCompClient import RecipeCompClient
from mod.server.component.timeCompServer import TimeComponentServer
from mod.server.component.actorOwnerCompServer import ActorOwnerComponentServer
from mod.client.component.playerViewCompClient import PlayerViewCompClient
from mod.server.component.projectileCompServer import ProjectileComponentServer
from mod.server.component.attrCompServer import AttrCompServer
from mod.client.component.queryVariableCompClient import QueryVariableComponentClient
from mod.server.component.redStoneCompServer import RedStoneComponentServer
from Preset.Model.PresetBase import PresetBase
from mod.common.component.baseComponent import BaseComponent
from mod.server.component.featureCompServer import FeatureCompServer
from mod.server.component.itemBannedCompServer import ItemBannedCompServer
from mod.server.component.breathCompServer import BreathCompServer
from mod.server.component.blockStateCompServer import BlockStateComponentServer
from mod.server.component.controlAiCompServer import ControlAiCompServer
from mod.client.component.engineTypeCompClient import EngineTypeComponentClient
from mod.client.component.chunkSourceCompClient import ChunkSourceCompClient
from mod.client.component.healthCompClient import HealthComponentClient
from mod.client.component.audioCustomCompClient import AudioCustomComponentClient
from mod.client.component.particleEntityBindComp import ParticleEntityBindComp
from mod.client.component.blockInfoCompClient import BlockInfoComponentClient
from mod.client.component.rotCompClient import RotComponentClient
from mod.server.component.explosionCompServer import ExplosionComponentServer
from mod.server.component.persistenceCompServer import PersistenceCompServer
from mod.server.component.portalCompServer import PortalComponentServer
from mod.server.component.commandCompServer import CommandCompServer
from mod.server.component.hurtCompServer import HurtCompServer
from mod.client.component.modelCompClient import ModelComponentClient
from mod.client.component.particleControlComp import ParticleControlComp
from typing import List
from mod.client.component.gameCompClient import GameComponentClient
from mod.server.component.recipeCompServer import RecipeCompServer
from mod.client.component.configCompClient import ConfigCompClient
from mod.client.component.nameCompClient import NameComponentClient
from mod.client.component.fogCompClient import FogCompClient
from mod.server.component.auxValueCompServer import AuxValueComponentServer
from mod.client.component.actorCollidableCompClient import ActorCollidableCompClient
from mod.client.component.brightnessCompClient import BrightnessCompClient
from mod.client.component.deviceCompClient import DeviceCompClient
from mod.server.component.entityEventCompServer import EntityEventComponentServer
from mod.server.component.playerCompServer import PlayerCompServer
from mod.server.component.actionCompServer import ActionCompServer
from mod.client.component.operationCompClient import OperationCompClient
from mod.client.component.modAttrCompClient import ModAttrComponentClient
from mod.server.component.moveToCompServer import MoveToComponentServer
from mod.server.component.modAttrCompServer import ModAttrComponentServer
from mod.server.component.exDataCompServer import ExDataCompServer
from mod.server.component.blockUseEventWhiteListCompServer import BlockUseEventWhiteListComponentServer
from mod.server.component.actorLootCompServer import ActorLootComponentServer
from mod.client.component.playerAnimCompClient import PlayerAnimCompClient

class PartBase(TransformObject):
    def __init__(self):
        # type: () -> None
        """
        PartBase（零件基类）是可以与零件进行绑定，而零件可以挂接在预设下，以实现带逻辑的预设的组装。所有的自定义零件都需要继承PartBase，预设系统下的大部分代码都需要写在自定义零件中。注意，自定义零件只有挂接到预设，并且在游戏中实例化才能生效。
        """
        self.tickEnable = None
        self.replicated = None
        self.system = None

    def InitClient(self):
        # type: () -> None
        """
        客户端的零件对象初始化入口
        """
        pass

    def InitServer(self):
        # type: () -> None
        """
        服务端的零件对象初始化入口
        """
        pass

    def TickClient(self):
        # type: () -> None
        """
        客户端的零件对象逻辑驱动入口
        """
        pass

    def TickServer(self):
        # type: () -> None
        """
        服务端的零件对象逻辑驱动入口
        """
        pass

    def UnloadClient(self):
        # type: () -> None
        """
        客户端的零件对象卸载逻辑入口
        """
        pass

    def UnloadServer(self):
        # type: () -> None
        """
        服务端的零件对象卸载逻辑入口
        """
        pass

    def DestroyClient(self):
        # type: () -> None
        """
        客户端的零件对象销毁逻辑入口
        """
        pass

    def DestroyServer(self):
        # type: () -> None
        """
        服务端的零件对象销毁逻辑入口
        """
        pass

    def CanAdd(self, parent):
        # type: (PresetBase) -> str
        """
        判断零件是否可以挂接到指定的父节点上
        """
        pass

    def GetTickCount(self):
        # type: () -> int
        """
        获取当前帧数
        """
        pass

    def ListenForEvent(self, namespace, systemName, eventName, instance, func, priority=0):
        # type: (str, str, str, object, object, str) -> None
        """
        监听指定的事件
        """
        pass

    def UnListenForEvent(self, namespace, systemName, eventName, instance, func, priority=0):
        # type: (str, str, str, object, object, str) -> None
        """
        反监听指定的事件
        """
        pass

    def DefineEvent(self, eventName):
        # type: (str) -> None
        """
        定义事件
        """
        pass

    def UnDefineEvent(self, eventName):
        # type: (str) -> None
        """
        反定义事件
        """
        pass

    def CreateEventData(self):
        # type: () -> dict
        """
        创建自定义事件的数据，eventData用于发送事件。创建的eventData可以理解为一个dict，可以嵌套赋值dict,list和基本数据类型，但不支持tuple
        """
        pass

    def BroadcastEvent(self, eventName, eventData):
        # type: (str, object) -> None
        """
        广播事件，双端通用
        """
        pass

    def BroadcastClientEvent(self, eventName, eventData):
        # type: (str, object) -> None
        """
        广播给所有客户端
        """
        pass

    def BroadcastServerEvent(self, eventName, eventData):
        # type: (str, object) -> None
        """
        广播给所有服务端
        """
        pass

    def NotifyToServer(self, eventName, eventData):
        # type: (str, object) -> None
        """
        通知服务端触发事件
        """
        pass

    def NotifyToClient(self, playerId, eventName, eventData):
        # type: (str, str, object) -> None
        """
        通知指定客户端触发事件
        """
        pass

    def BroadcastToAllClient(self, eventName, eventData):
        # type: (str, object) -> None
        """
        通知指所有客户端触发事件
        """
        pass

    def ListenSelfEvent(self, eventName, target, func):
        # type: (str, object, object) -> None
        """
        监听来自自己的事件
        """
        pass

    def UnListenSelfEvent(self, eventName, target, func):
        # type: (str, object, object) -> None
        """
        反监听来自自己的事件
        """
        pass

    def ListenPartEvent(self, partId, eventName, target, func):
        # type: (int, str, object, object) -> None
        """
        监听来自指定零件的事件
        """
        pass

    def UnListenPartEvent(self, partId, eventName, target, func):
        # type: (int, str, object, object) -> None
        """
        反监听来自指定零件的事件
        """
        pass

    def CreateComponent(self, entityId, nameSpace, name):
        # type: (Union[str,int], str, str) -> BaseComponent
        """
        给实体创建组件
        """
        pass

    def GetMinecraftEnum(self):
        """
        用于获取枚举值文档中的枚举值
        """
        return minecraftEnum

    def CreateAction(self, entityId):
        # type: (Union[str,int]) -> ActionCompServer
        """
        创建action组件
        """
        pass

    def SetMobKnockback(self, entityId, xd=0.1, zd=0.1, power=1.0, height=1.0, heightCap=1.0):
        # type: (Union[str,int], float, float, float, float, float) -> None
        """
        设置击退的初始速度，需要考虑阻力的影响
        """
        pass

    def CreateActorLoot(self, entityId):
        # type: (Union[str,int]) -> ActorLootComponentServer
        """
        创建actorLoot组件
        """
        pass

    def CreateActorMotion(self, entityId):
        # type: (Union[str,int]) -> Union[ActorMotionComponentServer,ActorMotionComponentClient]
        """
        创建actorMotion组件
        """
        pass

    def GetDirFromRot(self, rot):
        # type: (Tuple[float,float]) -> Tuple[float,float,float]
        """
        通过旋转角度获取朝向
        """
        pass

    def SetMotion(self, entityId, motion):
        # type: (Union[str,int], Tuple[float,float,float]) -> bool
        """
        设置生物（不含玩家）的瞬时移动方向向量
        """
        pass

    def CreateActorOwner(self, entityId):
        # type: (Union[str,int]) -> ActorOwnerComponentServer
        """
        创建actorOwner组件
        """
        pass

    def CreateActorPushable(self, entityId):
        # type: (Union[str,int]) -> ActorPushableCompServer
        """
        创建actorPushable组件
        """
        pass

    def CreateAttr(self, entityId):
        # type: (Union[str,int]) -> Union[AttrCompServer,AttrCompClient]
        """
        创建attr组件
        """
        pass

    def SetEntityOnFire(self, entityId, seconds, burn_damage=1):
        # type: (Union[str,int], int, int) -> bool
        """
        设置实体着火
        """
        pass

    def GetAttrValue(self, entityId, attrType):
        # type: (Union[str,int], int) -> float
        """
        获取属性值，包括生命值，饥饿度，移速
        """
        pass

    def GetAttrMaxValue(self, entityId, attrType):
        # type: (Union[str,int], int) -> float
        """
        获取属性最大值，包括生命值，饥饿度，移速
        """
        pass

    def SetAttrValue(self, entityId, attrType, value):
        # type: (Union[str,int], int, float) -> bool
        """
        设置属性值，包括生命值，饥饿度，移速
        """
        pass

    def SetAttrMaxValue(self, entityId, attrType, value):
        # type: (Union[str,int], int, float) -> bool
        """
        设置属性最大值，包括生命值，饥饿度，移速
        """
        pass

    def CreateAuxValue(self, entityId):
        # type: (Union[str,int]) -> Union[AuxValueComponentServer,AuxValueComponentClient]
        """
        创建auxValue组件
        """
        pass

    def CreateBiome(self, entityId):
        # type: (Union[str,int]) -> BiomeCompServer
        """
        创建biome组件
        """
        pass

    def CreateBlock(self, entityId):
        # type: (Union[str,int]) -> BlockCompServer
        """
        创建block组件
        """
        pass

    def CreateBlockEntityData(self, entityId):
        # type: (Union[str,int]) -> BlockEntityExDataCompServer
        """
        创建blockEntityData组件
        """
        pass

    def CreateBlockInfo(self, entityId):
        # type: (Union[str,int]) -> Union[BlockInfoComponentServer,BlockInfoComponentClient]
        """
        创建blockInfo组件
        """
        pass

    def GetBlock(self, pos, dimensionId=-1):
        # type: (Tuple[int,int,int], int) -> dict
        """
        获取某一位置的block
        """
        pass

    def SetBlockNew(self, pos, blockDict, oldBlockHandling=0, dimensionId=-1):
        # type: (Tuple[int,int,int], dict, int, int) -> bool
        """
        设置某一位置的方块
        """
        pass

    def CreateBlockState(self, entityId):
        # type: (Union[str,int]) -> BlockStateComponentServer
        """
        创建blockState组件
        """
        pass

    def CreateBlockUseEventWhiteList(self, entityId):
        # type: (Union[str,int]) -> Union[BlockUseEventWhiteListComponentServer,BlockUseEventWhiteListComponentClient]
        """
        创建blockUseEventWhiteList组件
        """
        pass

    def CreateBreath(self, entityId):
        # type: (Union[str,int]) -> BreathCompServer
        """
        创建breath组件
        """
        pass

    def CreateBulletAttributes(self, entityId):
        # type: (Union[str,int]) -> BulletAttributesComponentServer
        """
        创建bulletAttributes组件
        """
        pass

    def CreateChestBlock(self, entityId):
        # type: (Union[str,int]) -> ChestContainerCompServer
        """
        创建chestBlock组件
        """
        pass

    def CreateChunkSource(self, entityId):
        # type: (Union[str,int]) -> Union[ChunkSourceCompServer,ChunkSourceCompClient]
        """
        创建chunkSource组件
        """
        pass

    def CreateCollisionBox(self, entityId):
        # type: (Union[str,int]) -> CollisionBoxComponentServer
        """
        创建collisionBox组件
        """
        pass

    def CreateCommand(self, entityId):
        # type: (Union[str,int]) -> CommandCompServer
        """
        创建command组件
        """
        pass

    def SetCommand(self, cmdStr, playerId=None, showOutput=False):
        # type: (str, str, bool) -> bool
        """
        使用游戏内指令
        """
        pass

    def CreateControlAi(self, entityId):
        # type: (Union[str,int]) -> ControlAiCompServer
        """
        创建controlAi组件
        """
        pass

    def SetBlockControlAi(self, entityId, isBlock):
        # type: (Union[str,int], bool) -> bool
        """
        设置屏蔽生物原生AI
        """
        pass

    def CreateDimension(self, entityId):
        # type: (Union[str,int]) -> DimensionCompServer
        """
        创建dimension组件
        """
        pass

    def GetEntityDimensionId(self, entityId):
        # type: (Union[str,int]) -> int
        """
        获取实体所在维度
        """
        pass

    def ChangePlayerDimension(self, playerId, dimensionId, pos):
        # type: (Union[str,int], int, Tuple[int,int,int]) -> bool
        """
        传送玩家
        """
        pass

    def CreateEffect(self, entityId):
        # type: (Union[str,int]) -> EffectComponentServer
        """
        创建effect组件
        """
        pass

    def RemoveEffectFromEntity(self, entityId, effectName):
        # type: (Union[str,int], str) -> bool
        """
        为实体删除指定状态效果
        """
        pass

    def AddEffectToEntity(self, entityId, effectName, duration, amplifier, showParticles):
        # type: (Union[str,int], str, int, int, bool) -> bool
        """
        为实体添加指定状态效果，如果添加的状态已存在则有以下集中情况：1、等级大于已存在则更新状态等级及持续时间；2、状态等级相等且剩余时间duration大于已存在则刷新剩余时间；3、等级小于已存在则不做修改；4、粒子效果以新的为准
        """
        pass

    def CreateEngineType(self, entityId):
        # type: (Union[str,int]) -> Union[EngineTypeComponentServer,EngineTypeComponentClient]
        """
        创建engineType组件
        """
        pass

    def GetEngineTypeStr(self, entityId):
        # type: (Union[str,int]) -> str
        """
        获取实体的类型名称
        """
        pass

    def GetEngineType(self):
        # type: () -> int
        """
        获取实体类型
        """
        pass

    def CreateEntityEvent(self, entityId):
        # type: (Union[str,int]) -> EntityEventComponentServer
        """
        创建entityEvent组件
        """
        pass

    def TriggerCustomEvent(self, entityId, eventName):
        # type: (str, str) -> bool
        """
        触发生物自定义事件
        """
        pass

    def CreateExtraData(self, entityId):
        # type: (Union[str,int]) -> ExDataCompServer
        """
        创建extraData组件
        """
        pass

    def GetExtraData(self, key, entityId=None):
        # type: (str, str) -> Any
        """
        获取实体的自定义数据或者世界的自定义数据，某个键所对应的值。获取实体数据时使用对应实体id创建组件，获取世界数据时使用levelId创建组件
        """
        pass

    def SetExtraData(self, key, value, entityId=None, autoSave=True):
        # type: (str, Any, str, bool) -> bool
        """
        用于设置实体的自定义数据或者世界的自定义数据，数据以键值对的形式保存。设置实体数据时使用对应实体id创建组件，设置世界数据时使用levelId创建组件
        """
        pass

    def CleanExtraData(self, key, entityId=None):
        # type: (str, str) -> bool
        """
        清除实体的自定义数据或者世界的自定义数据，清除实体数据时使用对应实体id创建组件，清除世界数据时使用levelId创建组件
        """
        pass

    def CreateExp(self, entityId):
        # type: (Union[str,int]) -> ExpComponentServer
        """
        创建exp组件
        """
        pass

    def AddPlayerExperience(self, entityId, exp):
        # type: (Union[str,int], int) -> bool
        """
        增加玩家经验值
        """
        pass

    def CreateExplosion(self, entityId):
        # type: (Union[str,int]) -> ExplosionComponentServer
        """
        创建explosion组件
        """
        pass

    def CreateFeature(self, entityId):
        # type: (Union[str,int]) -> FeatureCompServer
        """
        创建feature组件
        """
        pass

    def CreateFly(self, entityId):
        # type: (Union[str,int]) -> FlyComponentServer
        """
        创建fly组件
        """
        pass

    def CreateGame(self):
        # type: () -> Union[GameComponentServer,GameComponentClient]
        """
        创建game组件
        """
        pass

    def KillEntity(self, entityId):
        # type: (str) -> bool
        """
        杀死某个Entity
        """
        pass

    def CreateEngineEntityByTypeStr(self, engineTypeStr, pos, rot, dimensionId=0, isNpc=False):
        # type: (str, Tuple[float,float,float], Tuple[float,float], int, bool) -> Union[str,None]
        """
        创建指定identifier的实体
        """
        pass

    def GetScreenSize(self):
        # type: () -> Tuple[float,float]
        """
        获取游戏分辨率
        """
        pass

    def PlaceStructure(self, pos, structureName, dimensionId=-1):
        # type: (Tuple[float,float,float], str, int) -> bool
        """
        放置结构
        """
        pass

    def AddTimer(self, delay, func, *args, **kwargs):
        # type: (float, function, Any, Any) -> CallLater
        """
        添加定时器，非重复
        """
        pass

    def AddRepeatedTimer(self, delay, func, *args, **kwargs):
        # type: (float, function, Any, Any) -> CallLater
        """
        添加服务端触发的定时器，重复执行
        """
        pass

    def CancelTimer(self, timer):
        # type: (CallLater) -> None
        """
        取消定时器
        """
        pass

    def GetEntitiesInSquareArea(self, startPos, endPos, dimensionId=-1):
        # type: (Tuple[int,int,int], Tuple[int,int,int], int) -> List[str]
        """
        获取区域内的entity列表
        """
        pass

    def GetEntitiesAround(self, entityId, radius, filters):
        # type: (str, int, dict) -> List[str]
        """
        获取区域内的entity列表
        """
        pass

    def ShowHealthBar(self, show):
        # type: (bool) -> bool
        """
        设置是否显示血条
        """
        pass

    def SetDisableHunger(self, isDisable):
        # type: (bool) -> bool
        """
        设置是否屏蔽饥饿度
        """
        pass

    def SetOneTipMessage(self, playerId, message):
        # type: (str, str) -> bool
        """
        在具体某个玩家的物品栏上方弹出tip类型通知，位置位于popup类型通知上方，此功能更建议在客户端使用game组件的对应接口SetTipMessage
        """
        pass

    def SetPopupNotice(self, message, subtitle):
        # type: (str, str) -> bool
        """
        在物品栏上方弹出popup类型通知，位置位于tip类型消息下方，服务端调用是针对全体玩家，客户端调用只影响本地玩家
        """
        pass

    def SetNotifyMsg(self, msg, color='\xc2\xa7f'):
        # type: (str, str) -> bool
        """
        设置消息通知
        """
        pass

    def GetPlayerGameType(self, playerId):
        # type: (str) -> int
        """
        获取指定玩家的游戏模式
        """
        pass

    def CreateGravity(self, entityId):
        # type: (Union[str,int]) -> GravityComponentServer
        """
        创建gravity组件
        """
        pass

    def SetGravity(self, entityId, gravity):
        # type: (Union[str,int], float) -> bool
        """
        设置实体的重力因子，当生物重力因子为0时则应用世界的重力因子
        """
        pass

    def CreateHurt(self, entityId):
        # type: (Union[str,int]) -> HurtCompServer
        """
        创建hurt组件
        """
        pass

    def SetHurtByEntity(self, entityId, attackerId, damage, byPassArmor, knocked=True):
        # type: (Union[str,int], str, int, bool, bool) -> bool
        """
        对实体造成伤害
        """
        pass

    def SetHurtByEntityNew(self, entityId, damage, cause, attackerId=None, childAttackerId=None, knocked=True):
        # type: (Union[str,int], int, str, str, str, bool) -> bool
        """
        对实体造成伤害
        """
        pass

    def CreateItemBanned(self, entityId):
        # type: (Union[str,int]) -> ItemBannedCompServer
        """
        创建itembanned组件
        """
        pass

    def CreateItem(self, entityId):
        # type: (Union[str,int]) -> Union[ItemCompServer,ItemCompClient]
        """
        创建item组件
        """
        pass

    def GetItemBasicInfo(self, itemName, auxValue=0, isEnchanted=False):
        # type: (str, int, bool) -> dict
        """
        获取物品的基础信息
        """
        pass

    def GetLocalPlayerId(self):
        # type: () -> str
        """
        获取本地玩家的id
        """
        pass

    def GetPlayerItem(self, playerId, posType, slotPos=0, getUserData=False):
        # type: (str, int, int, bool) -> dict
        """
        获取玩家物品，支持获取背包，盔甲栏，副手以及主手物品
        """
        pass

    def GetOffhandItem(self, playerId, getUserData=False):
        # type: (str, bool) -> dict
        """
        获取左手物品的信息
        """
        pass

    def SetInvItemNum(self, playerId, slotPos, num):
        # type: (str, int, int) -> bool
        """
        设置玩家背包物品数目
        """
        pass

    def SpawnItemToLevel(self, itemDict, dimensionId=0, pos=(0, 0, 0)):
        # type: (dict, int, Tuple[float,float,float]) -> bool
        """
        生成物品掉落物，如果需要获取物品的entityId，可以调用服务端系统接口CreateEngineItemEntity
        """
        pass

    def SpawnItemToPlayerInv(self, itemDict, playerId, slotPos=-1):
        # type: (dict, str, int) -> bool
        """
        生成物品到玩家背包
        """
        pass

    def SpawnItemToPlayerCarried(self, itemDict, playerId):
        # type: (dict, str) -> bool
        """
        生成物品到玩家右手
        """
        pass

    def GetCarriedItem(self, getUserData=False):
        # type: (bool) -> dict
        """
        获取右手物品的信息
        """
        pass

    def GetSlotId(self):
        # type: () -> int
        """
        获取当前手持的快捷栏的槽id
        """
        pass

    def CreateLv(self, entityId):
        # type: (Union[str,int]) -> LevelComponentServer
        """
        创建lv组件
        """
        pass

    def CreateMobSpawn(self, entityId):
        # type: (Union[str,int]) -> MobSpawnComponentServer
        """
        创建mobSpawn组件
        """
        pass

    def CreateModAttr(self, entityId):
        # type: (Union[str,int]) -> Union[ModAttrComponentServer,ModAttrComponentClient]
        """
        创建modAttr组件
        """
        pass

    def CreateModel(self, entityId):
        # type: (Union[str,int]) -> Union[ModelComponentServer,ModelComponentClient]
        """
        创建model组件
        """
        pass

    def PlayAnim(self, entityId, aniName, isLoop):
        # type: (Union[str,int], str, bool) -> bool
        """
        播放骨骼动画
        """
        pass

    def GetModelId(self):
        # type: () -> int
        """
        获取骨骼模型的Id，主要用于特效绑定骨骼模型
        """
        pass

    def SetModel(self, entityId, modelName):
        # type: (Union[str,int], str) -> bool
        """
        设置骨骼模型
        """
        pass

    def ResetModel(self, entityId):
        # type: (Union[str,int]) -> bool
        """
        设置骨骼模型
        """
        pass

    def BindModelToEntity(self, entityId, boneName, modelName):
        # type: (Union[str,int], str, str) -> int
        """
        实体替换骨骼模型后，再往上其他挂接骨骼模型。
        """
        pass

    def UnBindModelToEntity(self, entityId, modelId):
        # type: (Union[str,int], int) -> bool
        """
        取消实体上挂接的某个骨骼模型。取消挂接后，这个modelId的模型便会销毁，无法再使用，如果是临时隐藏可以使用HideModel
        """
        pass

    def CreateMoveTo(self, entityId):
        # type: (Union[str,int]) -> MoveToComponentServer
        """
        创建moveTo组件
        """
        pass

    def CreateMsg(self, entityId):
        # type: (Union[str,int]) -> MsgComponentServer
        """
        创建msg组件
        """
        pass

    def NotifyOneMessage(self, playerId, msg, color='\xc2\xa7f'):
        # type: (str, str, str) -> None
        """
        给指定玩家发送聊天框消息
        """
        pass

    def CreateName(self, entityId):
        # type: (Union[str,int]) -> Union[NameComponentServer,NameComponentClient]
        """
        创建name组件
        """
        pass

    def GetName(self, entityId):
        # type: (Union[str,int]) -> str
        """
        获取生物的自定义名称，即使用命名牌或者SetName接口设置的名称
        """
        pass

    def SetName(self, entityId, name):
        # type: (Union[str,int], str) -> bool
        """
        用于设置生物的自定义名称，跟原版命名牌作用相同，玩家和新版流浪商人暂不支持
        """
        pass

    def SetShowName(self, entityId, show):
        # type: (Union[str,int], bool) -> bool
        """
        设置生物名字是否按照默认游戏逻辑显示
        """
        pass

    def CreatePersistence(self, entityId):
        # type: (Union[str,int]) -> PersistenceCompServer
        """
        创建persistence组件
        """
        pass

    def CreatePet(self, entityId):
        # type: (Union[str,int]) -> PetComponentServer
        """
        创建pet组件
        """
        pass

    def CreatePlayer(self, entityId):
        # type: (Union[str,int]) -> PlayerCompServer
        """
        创建player组件
        """
        pass

    def GetPlayerHunger(self, playerId):
        # type: (Union[str,int]) -> float
        """
        获取玩家饥饿度，展示在UI饥饿度进度条上，初始值为20，即每一个鸡腿代表2个饥饿度。 **饱和度(saturation)** ：玩家当前饱和度，初始值为5，最大值始终为玩家当前饥饿度(hunger)，该值直接影响玩家**饥饿度(hunger)**。<br>1）增加方法：吃食物。<br>2）减少方法：每触发一次**消耗事件**，该值减少1，如果该值不大于0，直接把玩家 **饥饿度(hunger)** 减少1。
        """
        pass

    def CreatePortal(self, entityId):
        # type: (Union[str,int]) -> PortalComponentServer
        """
        创建portal组件
        """
        pass

    def CreatePos(self, entityId):
        # type: (Union[str,int]) -> Union[PosComponentServer,PosComponentClient]
        """
        创建pos组件
        """
        pass

    def GetPos(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float,float]
        """
        获取实体位置
        """
        pass

    def GetFootPos(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float,float]
        """
        获取实体脚所在的位置
        """
        pass

    def SetPos(self, entityId, pos):
        # type: (Union[str,int], Tuple[int,int,int]) -> bool
        """
        设置实体位置
        """
        pass

    def CreateProjectile(self, entityId):
        # type: (Union[str,int]) -> ProjectileComponentServer
        """
        创建projectile组件
        """
        pass

    def CreateRecipe(self, entityId):
        # type: (Union[str,int]) -> Union[RecipeCompServer,RecipeCompClient]
        """
        创建recipe组件
        """
        pass

    def CreateRedStone(self, entityId):
        # type: (Union[str,int]) -> RedStoneComponentServer
        """
        创建redStone组件
        """
        pass

    def CreateRide(self, entityId):
        # type: (Union[str,int]) -> RideCompServer
        """
        创建ride组件
        """
        pass

    def CreateRot(self, entityId):
        # type: (Union[str,int]) -> Union[RotComponentServer,RotComponentClient]
        """
        创建rot组件
        """
        pass

    def GetRot(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float]
        """
        获取实体角度
        """
        pass

    def SetRot(self, entityId, rot):
        # type: (Union[str,int], Tuple[float,float]) -> bool
        """
        设置实体的头的角度
        """
        pass

    def CreateScale(self, entityId):
        # type: (Union[str,int]) -> ScaleComponentServer
        """
        创建scale组件
        """
        pass

    def CreateTame(self, entityId):
        # type: (Union[str,int]) -> TameComponentServer
        """
        创建tame组件
        """
        pass

    def CreateTime(self, entityId):
        # type: (Union[str,int]) -> TimeComponentServer
        """
        创建time组件
        """
        pass

    def GetTime(self):
        # type: () -> int
        """
        获取当前世界时间
        """
        pass

    def CreateWeather(self, entityId):
        # type: (Union[str,int]) -> WeatherComponentServer
        """
        创建weather组件
        """
        pass

    def CreateActorCollidable(self, entityId):
        # type: (Union[str,int]) -> ActorCollidableCompClient
        """
        创建actorCollidable组件
        """
        pass

    def CreateActorRender(self, entityId):
        # type: (Union[str,int]) -> ActorRenderCompClient
        """
        创建actorRender组件
        """
        pass

    def CreateCustomAudio(self, entityId):
        # type: (Union[str,int]) -> AudioCustomComponentClient
        """
        创建customAudio组件
        """
        pass

    def CreateBrightness(self, entityId):
        # type: (Union[str,int]) -> BrightnessCompClient
        """
        创建brightness组件
        """
        pass

    def CreateCamera(self, entityId):
        # type: (Union[str,int]) -> CameraComponentClient
        """
        创建camera组件
        """
        pass

    def PickFacing(self):
        # type: () -> dict
        """
        获取准星选中的实体或者方块
        """
        pass

    def CreateFog(self, entityId):
        # type: (Union[str,int]) -> FogCompClient
        """
        创建fog组件
        """
        pass

    def CreateFrameAniControl(self, entityId):
        # type: (Union[str,int]) -> FrameAniControlComp
        """
        创建frameAniControl组件
        """
        pass

    def SetFrameAniLoop(self, entityId, loop):
        # type: (Union[str,int], bool) -> bool
        """
        设置序列帧是否循环播放，默认为否
        """
        pass

    def SetFrameAniFaceCamera(self, entityId, face):
        # type: (Union[str,int], bool) -> bool
        """
        设置序列帧是否始终朝向摄像机，默认为是
        """
        pass

    def SetFrameAniDeepTest(self, entityId, deepTest):
        # type: (Union[str,int], bool) -> bool
        """
        设置序列帧是否透视，默认为否
        """
        pass

    def CreateFrameAniEntityBind(self, entityId):
        # type: (Union[str,int]) -> FrameAniEntityBindComp
        """
        创建frameAniEntityBind组件
        """
        pass

    def CreateFrameAniSkeletonBind(self, entityId):
        # type: (Union[str,int]) -> FrameAniSkeletonBindComp
        """
        创建frameAniSkeletonBind组件
        """
        pass

    def CreateFrameAniTrans(self, entityId):
        # type: (Union[str,int]) -> FrameAniTransComp
        """
        创建frameAniTrans组件
        """
        pass

    def GetFrameAniPos(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float,float]
        """
        获取序列帧位置
        """
        pass

    def GetFrameAniRot(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float]
        """
        获取序列帧的角度
        """
        pass

    def GetFrameAniScale(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float,float]
        """
        获取序列帧的缩放
        """
        pass

    def SetFrameAniPos(self, entityId, pos):
        # type: (Union[str,int], Tuple[int,int,int]) -> bool
        """
        设置序列帧位置
        """
        pass

    def SetFrameAniRot(self, entityId, rot):
        # type: (Union[str,int], Tuple[float,float]) -> bool
        """
        设置特效的角度
        """
        pass

    def SetFrameAniScale(self, entityId, scale):
        # type: (Union[str,int], Tuple[float,float,float]) -> bool
        """
        设置序列帧的缩放
        """
        pass

    def CreateHealth(self, entityId):
        # type: (Union[str,int]) -> HealthComponentClient
        """
        创建health组件
        """
        pass

    def ShowHealth(self, entityId, show):
        # type: (Union[str,int], bool) -> None
        """
        设置某个entity是否显示血条，默认为显示
        """
        pass

    def CreateOperation(self, entityId):
        # type: (Union[str,int]) -> OperationCompClient
        """
        创建operation组件
        """
        pass

    def SetCanAll(self, all):
        # type: (bool) -> bool
        """
        同时设置SetCanMove，SetCanJump，SetCanAttack，SetCanWalkMode，SetCanPerspective，SetCanPause，SetCanChat，SetCanScreenShot，SetCanOpenInv，SetCanDrag，SetCanInair
        """
        pass

    def CreateDevice(self, entityId):
        # type: (Union[str,int]) -> DeviceCompClient
        """
        创建device组件
        """
        pass

    def CreateParticleControl(self, entityId):
        # type: (Union[str,int]) -> ParticleControlComp
        """
        创建particleControl组件
        """
        pass

    def CreateParticleEntityBind(self, entityId):
        # type: (Union[str,int]) -> ParticleEntityBindComp
        """
        创建particleEntityBind组件
        """
        pass

    def CreateParticleSkeletonBind(self, entityId):
        # type: (Union[str,int]) -> ParticleSkeletonBindComp
        """
        创建particleSkeletonBind组件
        """
        pass

    def CreateParticleTrans(self, entityId):
        # type: (Union[str,int]) -> ParticleTransComp
        """
        创建particleTrans组件
        """
        pass

    def GetParticlePos(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float,float]
        """
        获取特效位置
        """
        pass

    def GetParticleRot(self, entityId):
        # type: (Union[str,int]) -> Tuple[float,float]
        """
        获取特效角度
        """
        pass

    def SetParticlePos(self, entityId, pos):
        # type: (Union[str,int], Tuple[int,int,int]) -> bool
        """
        设置特效位置
        """
        pass

    def SetParticleRot(self, entityId, rot):
        # type: (Union[str,int], Tuple[float,float]) -> bool
        """
        设置特效的角度
        """
        pass

    def CreatePlayerView(self, entityId):
        # type: (Union[str,int]) -> PlayerViewCompClient
        """
        创建playerView组件
        """
        pass

    def GetPerspective(self, playerId):
        # type: (Union[str,int]) -> int
        """
        获取当前的视角模式
        """
        pass

    def SetPerspective(self, playerId, persp):
        # type: (Union[str,int], int) -> bool
        """
        设置视角模式
        """
        pass

    def CreateQueryVariable(self, entityId):
        # type: (Union[str,int]) -> QueryVariableComponentClient
        """
        创建queryVariable组件
        """
        pass

    def CreateSkyRender(self, entityId):
        # type: (Union[str,int]) -> SkyRenderCompClient
        """
        创建skyRender组件
        """
        pass

    def CreateTextBoard(self, entityId):
        # type: (Union[str,int]) -> TextBoardComponentClient
        """
        创建textBoard组件
        """
        pass

    def CreateTextNotifyClient(self, entityId):
        # type: (Union[str,int]) -> TextNotifyComponet
        """
        创建textNotifyClient组件
        """
        pass

    def CreateConfigClient(self, levelId):
        # type: (str) -> ConfigCompClient
        """
        创建config组件
        """
        pass

    def CreateVirtualWorld(self, levelId):
        # type: (str) -> VirtualWorldCompClient
        """
        创建virtualWorld组件实例组件
        """
        pass

    def CreatePlayerAnim(self, playerId):
        # type: (str) -> PlayerAnimCompClient
        """
        创建玩家动画组件
        """
        pass

