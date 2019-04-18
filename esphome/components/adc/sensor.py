import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import sensor
from esphome.const import CONF_ATTENUATION, CONF_ID, CONF_PIN, ICON_FLASH, UNIT_VOLT

ATTENUATION_MODES = {
    '0db': cg.global_ns.ADC_0db,
    '2.5db': cg.global_ns.ADC_2_5db,
    '6db': cg.global_ns.ADC_6db,
    '11db': cg.global_ns.ADC_11db,
}


def validate_adc_pin(value):
    vcc = str(value).upper()
    if vcc == 'VCC':
        return cv.only_on_esp8266(vcc)
    return pins.analog_pin(value)


adc_ns = cg.esphome_ns.namespace('adc')
ADCSensor = adc_ns.class_('ADCSensor', sensor.PollingSensorComponent)

CONFIG_SCHEMA = sensor.sensor_schema(UNIT_VOLT, ICON_FLASH, 2).extend({
    cv.GenerateID(): cv.declare_variable_id(ADCSensor),
    cv.Required(CONF_PIN): validate_adc_pin,
    cv.SplitDefault(CONF_ATTENUATION, esp32='0db'):
        cv.All(cv.only_on_esp32, cv.enum(ATTENUATION_MODES, lower=True)),
}).extend(cv.polling_component_schema('60s'))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield sensor.register_sensor(var, config)

    if config[CONF_PIN] == 'VCC':
        cg.add_define('USE_ADC_SENSOR_VCC')
        cg.add_global(cg.global_ns.ADC_MODE(cg.global_ns.ADC_VCC))
    else:
        cg.add(var.set_pin(config[CONF_PIN]))

    if CONF_ATTENUATION in config:
        cg.add(var.set_attenuation(config[CONF_ATTENUATION]))
