#pragma once

#include "esphome/core/component.h"
#include "esphome/core/esphal.h"
#include "esphome/components/display/display_buffer.h"

namespace esphome {
namespace ssd1325_base {

enum SSD1325Model {
  SSD1325_MODEL_128_32 = 0,
  SSD1325_MODEL_128_64,
  SSD1325_MODEL_96_16,
  SSD1325_MODEL_64_48,
  SSD1327_MODEL_128_128,
};

class SSD1325 : public PollingComponent, public display::DisplayBuffer {
 public:
  void setup() override;

  void display();

  void update() override;

  void set_model(SSD1325Model model) { this->model_ = model; }
  void set_reset_pin(GPIOPin *reset_pin) { this->reset_pin_ = reset_pin; }
  void set_external_vcc(bool external_vcc) { this->external_vcc_ = external_vcc; }

  float get_setup_priority() const override { return setup_priority::PROCESSOR; }
  void fill(int color) override;

 protected:
  virtual void command(uint8_t value) = 0;
  virtual void write_display_data() = 0;
  void init_reset_();

  void draw_absolute_pixel_internal(int x, int y, int color) override;

  int get_height_internal() override;
  int get_width_internal() override;
  size_t get_buffer_length_();
  const char *model_str_();

  SSD1325Model model_{SSD1325_MODEL_128_64};
  GPIOPin *reset_pin_{nullptr};
  bool external_vcc_{false};
};

}  // namespace ssd1325_base
}  // namespace esphome
