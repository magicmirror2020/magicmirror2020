/* Magic Mirror Config Sample
 *
 * By Michael Teeuw http://michaelteeuw.nl
 * MIT Licensed.
 *
 * For more information on how you can configure this file
 * See https://github.com/MichMich/MagicMirror#configuration
 *
 */

var config = {
	address: "0.0.0.0",
	port: 8080,
	ipWhitelist: [], // ["127.0.0.1", "::ffff:127.0.0.1", "::1","192.168.0.1/24"],     
							       // ["127.0.0.1", "::ffff:127.0.0.1", "::1"], // Set [] to allow all IP addresses
	                                                       // or add a specific IPv4 of 192.168.1.5 :
	                                                       // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.1.5"],
	                                                       // or IPv4 range of 192.168.3.0 --> 192.168.3.15 use CIDR format :
	                                                       // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.3.0/28"],

	useHttps: false, 	// Support HTTPS or not, default "false" will use HTTP
	httpsPrivateKey: "", 	// HTTPS private key path, only require when useHttps is true
	httpsCertificate: "", 	// HTTPS Certificate path, only require when useHttps is true

	language: "en",
	timeFormat: 24,
	units: "metric",
	// serverOnly:  true/false/"local" ,
			     // local for armv6l processors, default
			     //   starts serveronly and then starts chrome browser
			     // false, default for all  NON-armv6l devices
			     // true, force serveronly mode, because you want to.. no UI on this device

	modules: [
		{
			module: 'MMM-Cursor'
		},
		//{	module: 'compliments',
		//	position: 'bottom_bar'
		//},
		//{
		//	module: "updatenotification",
		//	position: "top_bar"
		//},
		{
			module: "clock",
			position: "bottom_left"
		},
		{
    			module: 'MMM-Remote-Control',
 	 		//position: 'top_left',
    			config: {
        			customCommand: {},  // Optional, See "Using Custom Commands" below
        			customMenu: "custom_menu.json", // Optional, See "Custom Menu Items" below
        			showModuleApiMenu: true // Optional, Enable the Module Controls menu

    			}
		},
		{
		      module: 'MMM-pages',
 			config: {
				modules:
                    		[[ "MMM-Weather-Now", "weatherforecast", "MMM-News", "MMM-Spotify", "clock", "MMM-AVStock"],
                    		["MMM-MyStandings", "MMM-Bob-Ross", "MMM-DailyDilbert"]], //"MMM-Globe"
                		fixed: ["MMM-page-indicator"],
        			}
    		},
		{
        		module: 'MMM-page-indicator',
        		position: 'bottom_bar',
        		config: {
            			pages: 2,
        		}
    		},
		//{
		//	module: "currentweather",
		//	position: "top_left",
		//	header: "",
		//	config: {
		//		location: "",
		//		locationID: "4143861",  //ID from http://www.openweathermap.org/help/city_list.txt
		//		appid: "0b72791793bc48c41a5641b96e4ef00a",
		//		units: "imperial", // default` = Kelvin, `metric` = Celsius, `imperial` =Fahrenheit 
		//		// your other options can go here. Just remove this line
		//	}
		//},
		{
			module: 'MMM-Weather-Now',
			position:'top_left',
			config: {
				api_key:    '543d54240d3e44e5bed9f7150ca3e0cd',
				lat:		39.6837226,
				lon:		-75.7496572,
				units:		'I',
				lang:		'en',
				interval:   900000
			}
		},
		{
                	module: "weatherforecast",
			position: "top_left",
			header: "",
			config: {
				location: "",
				locationID: "4143861",  //ID from http://www.openweathermap.org/help/city_list.txt
				appid: "0b72791793bc48c41a5641b96e4ef00a",
				units: "imperial" // default` = Kelvin, `metric` = Celsius, `imperial` =Fahrenheit
				// your other options can go here. Just remove this line
			}
		},
		{
			module: "MMM-News",
  			position: "top_right",
  			config: {
    			apiKey : "1fda2d32e0254bfc84eca6ebeb68c9f2",
    			type: "vertical",
    			query : [
      				{sources: "msnbc,bloomberg",},
      				{country: "us",className: "redTitle",},
      				{country: "us",category: "health",q : "coronavirus"}
    				],
  			}
		},
		{
  			module: "MMM-Spotify",
  			position: "bottom_left",
  			config: {
    				style: "mini",
    				control: "default",
    				updateInterval: 1000
  			}
		},
		{
  			module: "MMM-AVStock",
  			position: "bottom_right", //"bottom_bar" is better for `mode:ticker`
  			config: {
    				apiKey : "WVW918TI81QHKT4B", // https://www.alphavantage.co/
    				timeFormat: "YYYY-MM-DD HH:mm:ss",
    				symbols : ["aapl", "GOOGL", "005930.KS"],
    				alias: ["APPLE", "", "SAMSUNG Electronics"], //Easy name of each symbol. When you use `alias`, the number of symbols and alias should be the same. If value is null or "", symbol string will be used by default.
    				tickerDuration: 60, // Ticker will be cycled once per this second.
    				chartDays: 90, //For `mode:series`, how much daily data will be taken. (max. 90)
    				poolInterval : 1000*15, // (Changed in ver 1.1.0) - Only For Premium Account
    				mode : "table", // "table", "ticker", "series"
    				decimals: 4, // number o decimals for all values including decimals (prices, price changes, change%...)
    				candleSticks : false, //show candle sticks if mode is Series
    				coloredCandles : false, //colored bars: red and green for negative and positive candles
    				premiumAccount: false, // To change poolInterval, set this to true - Only For Premium Account
  			}
		},
		{
      			module: "MMM-Bob-Ross",
      			position: "bottom_right",
      			config: {
        			imgHeight: "30vh", //Or any valid css height measure. Defines the height of the painting.
        			videoHeight: "30vh", //Same as above. Defines the height of the video
        			updateInterval: 1*60*60*1000, //How often does the painting change?
        			autoPlay: true //Should the video start as soon as it switches or does it need the play command?
      				}
    		},
		//{
		//	module: 'MMM-Globe',
		//	position: 'top_left',
		//	config: {
		//		style: 'natColor',
		//		imageSize: 300,
		//		ownImagePath:'',
		//		updateInterval: 10*60*1000
		//	}
		//},
		{
    			module: 'MMM-DailyDilbert',
			position: 'bottom_left',
			config: {
				updateInterval : 36000000
			}
 		},
		{
			module: "MMM-MyStandings",
			position: "top_right",
			config: {
				updateInterval: 60 * 60 * 1000, // every 60 minutes
				rotateInterval: 0.10 * 60 * 1000, // every 1 minute
				sports: [
					{ league: "NBA", groups: ["Atlantic", "Central", "Southeast", "Northwest", "Pacific", "Southwest"] },
					{ league: "MLB", groups: ["American League East", "American League Central", "American League West", "National League East", "National League Central", "National League West"] },
					{ league: "NFL", groups: ["AFC East", "AFC North", "AFC South", "AFC West", "NFC East", "NFC North", "NFC South", "NFC West"] },
					{ league: "NHL", groups: ["Atlantic Division", "Metropolitan Division", "Central Division", "Pacific Division"] },
					],
				nameStyle: "short",
				showLogos: true,
				useLocalLogos: true,
				showByDivision: true,
				fadeSpeed: 2000,
			}
  		}
	]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
