import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import uart
from esphome.const import CONF_ID, CONF_UART_ID, CONF_ON_TAG, CONF_TRIGGER_ID

DEPENDENCIES = ['uart']
AUTO_LOAD = ['binary_sensor']

rdm6300_ns = cg.esphome_ns.namespace('rdm6300')
RDM6300Component = rdm6300_ns.class_('RDM6300Component', cg.Component, uart.UARTDevice)
RDM6300Trigger = rdm6300_ns.class_('RDM6300Trigger', cg.Trigger.template(cg.uint32))

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_variable_id(RDM6300Component),
    cv.GenerateID(CONF_UART_ID): cv.use_variable_id(uart.UARTComponent),
    cv.Optional(CONF_ON_TAG): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_variable_id(RDM6300Trigger),
    }),
}).extend(cv.COMPONENT_SCHEMA)


def to_code(config):
    uart_ = yield cg.get_variable(config[CONF_UART_ID])
    var = cg.new_Pvariable(config[CONF_ID], uart_)
    yield cg.register_component(var, config)

    for conf in config.get(CONF_ON_TAG, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID])
        cg.add(var.register_trigger(trigger))
        yield automation.build_automation(trigger, [(cg.uint32, 'x')], conf)
