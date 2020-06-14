$(()=>{
	// influx();
});

influx = ()=>{
	// const {InfluxDB} = require('@influxdata/influxdb-client');
	  import {InfluxDB, Point} from 'https://unpkg.com/@influxdata/influxdb-client/dist/index.browser.mjs';
	  import {HealthAPI, SetupAPI} from 'https://unpkg.com/@influxdata/influxdb-client-apis/dist/index.browser.mjs';

	// You can generate a Token from the "Tokens Tab" in the UI
	const token = 'okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg==';
	const org = 'cos301.alpha@gmail.com';
	const bucket = 'test Bucket';

	const client = new InfluxDB({url: 'https://eu-central-1-1.aws.cloud2.influxdata.com', token: token});

	//Read from database
	const queryApi = client.getQueryApi(org);
	    console.log("echo");

	const query = `from(bucket: "${bucket}") |> range(start: -1h)`;
	queryApi.queryRows(query, {
	  next(row, tableMeta) {
	    const o = tableMeta.toObject(row);
	    console.log(
	      `${o._time} ${o._measurement} in '${o.location}' (${o.example}): ${o._field}=${o._value}`
	    );
	  },
	  error(error) {
	    console.error(error);
	    console.log('\nFinished ERROR');
	  },
	  complete() {
	    console.log('\nFinished SUCCESS');
	  },
	});
}