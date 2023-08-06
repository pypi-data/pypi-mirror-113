from enum import Enum


class IssueModule(str, Enum):
    EMOTIBOT_CONTROLLER = "emotibot-controller"
    SSM_DAC = "ssm-dac"
    FAQ_PREDICT = "faq-predict"
    ML_PLATFORM_ON_LINE = "ml-platform-online"
    ML_PLATFORM_OFF_LINE = "ml-platform-offline"
    ML = "ml"
    ML_TRAIN = "ml-train"
    BM = "bm"


class PipeType(str, Enum):
    FAQ_PREDIC_PIPE = "faq_predict_pipe"
    FAQ_TRAIN_PIPE = "faq_train_pipe"
