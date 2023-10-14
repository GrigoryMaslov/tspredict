from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import prediction
import jax
from flax import linen as nn

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class myLSTM(nn.Module):
  features: int

  def setup(self):
    self.scan_cell = nn.scan(
      nn.OptimizedLSTMCell,
      variable_broadcast='params',
      in_axes=1, out_axes=1,
      split_rngs={'params': False})(self.features)
    self.attention = nn.MultiHeadDotProductAttention(num_heads=1)

  @nn.compact
  def __call__(self, x):
    (carry, hidden) = self.scan_cell.initialize_carry(jax.random.key(0), x[:, 0].shape)
    (carry, hidden), x = self.scan_cell((carry, hidden), x)
    x = self.attention(inputs_q=x, inputs_kv=x)
    x = nn.Dense(32)(x[:,0,:])
    x = nn.relu(x)
    x = nn.Dense(3)(x)
    return x

class Test(Resource):
    def get(self):
        return 'Server for the TS prediction model'

    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201

            return {"error":"Invalid format."}

        except Exception as error:
            return {'error': error}

class GetPredictionOutput(Resource):
    def get(self):
        return {"error":"Invalid Method."}

    def post(self):
        try:
            data = request.get_json()
            predict = prediction.predict_mpg(data)
            predictOutput = predict
            return {'predict':predictOutput}

        except Exception as error:
            return {'error': error}

api.add_resource(Test,'/')
api.add_resource(GetPredictionOutput,'/getPredictionOutput')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)