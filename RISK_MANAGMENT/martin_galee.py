from templates import TEMPLATES
import os
current_file = os.path.basename(__file__)

class MARTIN_GALE(TEMPLATES):
    def __init__(self):  
        super().__init__()
        self.max_martin_gale_counter_func = self.log_exceptions_decorator(self.max_martin_gale_counter_func)
        self.martin_gale_prosess_handler = self.log_exceptions_decorator(self.martin_gale_prosess_handler) 
        self.is_martin_gale_true_template = self.log_exceptions_decorator(self.is_martin_gale_true_template) 
    
    def max_martin_gale_counter_func(self, depo, static_stop_loss_ratio_val, total_usdt_ammount, martin_gale_ratio, leverage):        
        martin_counter = 0
        total_loses = 0

        while True:
            martin_counter += 1 
            cur_losses = depo*leverage*(static_stop_loss_ratio_val/100)*(martin_gale_ratio)**martin_counter            
            total_loses += cur_losses            
            if depo*(martin_gale_ratio)**martin_counter >= total_usdt_ammount - total_loses:                          
                return martin_counter-1, total_loses
            # print(cur_losses)
    
    def martin_gale_prosess_handler(self, last_win_los, start_depo, depo, cur_martin_gale_counter, max_martin_gale_counter, martin_gale_ratio):
        if (cur_martin_gale_counter == max_martin_gale_counter) or (last_win_los == 1):
            cur_martin_gale_counter = 0
            depo = start_depo
            self.handle_messagee(f"Размер депозита был сброшен до начального и составляет: {depo}") 
            return depo, cur_martin_gale_counter
        if last_win_los == -1:
            depo = round(depo*martin_gale_ratio, 2)
            cur_martin_gale_counter += 1
            self.handle_messagee(f"Размер депозита был изменен и составляет: {depo}\n Tекущий Мартин Гейл счетчик равен {cur_martin_gale_counter}")
        return depo, cur_martin_gale_counter
    
    def is_martin_gale_true_template(self):
        total_usdt_ammount = None
        if self.martin_gale_flag:   
            total_usdt_ammount = self.get_total_balance('USDT')
            # print(total_usdt_ammount)
            if total_usdt_ammount is not None and isinstance(total_usdt_ammount, float):
                self.max_martin_gale_counter, self.total_potential_losses = self.max_martin_gale_counter_func(self.depo, self.static_stop_loss_ratio_val, total_usdt_ammount, self.martin_gale_ratio, self.lev_size)           
                self.handle_messagee(f"Можем умножать депозит по Мартин Гейлу {self.max_martin_gale_counter} раз")       
                self.handle_messagee(f"Потенциально максимальный убыток в случае худшего сценария Мартин Гейла: {self.total_potential_losses} usdt")
            elif total_usdt_ammount == 0:
                self.handle_messagee(f"Баланс usdt = 0. Нет возможности произвести расчеты Мартин Гейла")     
            else:
                self.handle_messagee(f"Не удалось получить данные баланса")
                
# python -m RISK_MANAGMENT.martin_galee