const puppeteer = require("puppeteer");

async function start(){

 const browser = await puppeteer.launch({
  headless:true,
  args:["--no-sandbox","--disable-setuid-sandbox"]
 });

 const page = await browser.newPage();

 // COOKIE QO‘SHISH
 await page.setCookie(
 {
  name:"user_session",
  value:"uanmls56krsgudjrvogm2kqr0k5sm8ka",
  domain:"litepick.io",
  path:"/"
 },
 {
  name:"remember_token",
  value:"b2dd75a43d5992b141b46b188638b4dd",
  domain:"litepick.io",
  path:"/"
 },
 {
  name:"csrf_cookie_name",
  value:"e4a8adb530b21b9a44a9ec5336141908",
  domain:"litepick.io",
  path:"/"
 },
 {
  name:"fp",
  value:"HRLWQ3ce0fkXU5u6",
  domain:"litepick.io",
  path:"/"
 }
 );

 while(true){

  try{

   console.log("Litepick ochilmoqda...");

   await page.goto("https://litepick.io/faucet.php",{waitUntil:"networkidle2"});

   await page.waitForTimeout(5000);

   const btn = await page.$("#process_claim_hourly_faucet");

   if(btn){

    console.log("Claim mavjud → bosilmoqda");

    await btn.click();

   }else{

    console.log("Claim hali mavjud emas");

   }

  }catch(err){

   console.log("Xato:",err.message);

  }

  console.log("61 minut kutish...");
  await page.waitForTimeout(61*60*1000);

 }

}

start();
