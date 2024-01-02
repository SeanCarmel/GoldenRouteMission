<template>
  <div>
  <h2>Enter mass of cargo</h2>
    <div class="calculator">
      <div class="display">{{ current || '0' }}</div>
      <div @click="append('7')" class="button">7</div>
      <div @click="append('8')" class="button">8</div>
      <div @click="append('9')" class="button">9</div>
      <div @click="append('4')" class="button">4</div>
      <div @click="append('5')" class="button">5</div>
      <div @click="append('6')" class="button">6</div>
      <div @click="append('1')" class="button">1</div>
      <div @click="append('2')" class="button">2</div>
      <div @click="append('3')" class="button">3</div>
      <div @click="enter" class="enter_btn" >Enter</div>
      <div @click="zero_btn()" class="button">0</div>
      <div @click="dot" class="button">.</div>
      <div @click="clear" class="special_btn">C</div>
      <div @click="del" class="special_btn">del</div>
    </div>
    <br><br>
    <div class="alert alert-danger alert-dismissible" role="alert" v-if="show_tempature_msg_danger">
      <div>{{tempature_msg}} </div>
      <button type="button" @click="show_tempature_msg_danger=false" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="alert alert-success alert-dismissible" role="alert" v-if="show_calc_msg_success && show_tempature_msg_success">
      <div>{{ calc_msg }}</div>
      <button type="button" @click="show_calc_msg_success=false" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="alert alert-warning alert-dismissible" role="alert" v-if="show_clac_msg_warning && show_tempature_msg_success">
      <div>{{ calc_msg }}</div>
      <button type="button" @click="show_clac_msg_warning=false" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="alert alert-success alert-dismissible" role="alert" v-if="show_calc_msg_success && show_tempature_msg_success">
      <div>{{tempature_msg}} </div>
      <button type="button" @click="show_tempature_msg_success=false" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      current: '',
      calc_msg: '',
      tempature_msg: '',
      show_calc_msg_success : false,
      show_clac_msg_warning : false,
      show_tempature_msg_danger : false,
      show_tempature_msg_success: false
    }
  },
  methods: {
    reset() {
      this.show_calc_msg_success = false
      this.show_clac_msg_warning = false
      this.show_tempature_msg_danger = false
      this.show_tempature_msg_success = false
    },
    clear() {
      this.reset()
      this.current = '';
    },
    append(number) {
      this.reset()
      this.current = `${this.current}${number}`;
    },
    zero_btn() {
      this.reset()
      if (this.current !== '0' && this.current !== ''){
        this.append('0');
      }
    },
    dot() {
      if (this.current.indexOf('.') === -1) {
        if (this.current === '')
          this.append('0');
        this.append('.');
      }
    },
    del() {
      this.reset()
      this.current = this.current.slice(0, -1);
    },
    enter() {
      if (this.current == '')
      {
        this.current = '0'
        this.reset()
      }
      this.get_tempature()
      this.get_calc_msg(this.current)
      this.current = ''
    },
    async get_calc_msg(cargo_mass) {
      const path = `http://localhost:5001/calculating/${cargo_mass}`;
      axios.get(path)
        .then(async (res) => {
          this.calc_msg = await res.data.calc_result;
          if (this.calc_msg.includes("destroy"))
            this.show_clac_msg_warning = true
          else if (this.calc_msg.includes("distance"))
            this.show_calc_msg_success = true
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async get_tempature() {
      const path = `http://localhost:5001/checkWeather`;
      axios.get(path)
        .then(async (res) => {
          this.tempature_msg = await res.data.weather_result;
          if (this.tempature_msg.includes('tempatures'))
            this.show_tempature_msg_danger = true
          else
            this.show_tempature_msg_success = true
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
}
</script>

<style>
#app
{
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 0px;
  font-size: 20px;
}
.calculator {
  font-size: 35px;
  margin: 0 auto;
  width: 400px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: minmax(50px, auto);
  align-items: center;
  justify-content: center;
}
.display {
  font-size: 35px;
  grid-column: 1 / 4;
  background-color: black;
  color: white;
}
.button {
  font-size: 35px;
  background-color: #9eceff;
  color: black;
  border: 1px solid black;
}
.special_btn {
  font-size: 35px;
  background-color: #9eceff;
  color: #22229b;
  border: 1px solid black;
}
.enter_btn {
  font-size: 35px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  grid-row: 5/7;
  grid-column: 1;
  background-color: #22229b;
  color: white;
  border: 1px solid black;
}
</style>






