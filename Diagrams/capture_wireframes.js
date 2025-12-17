const puppeteer = require('puppeteer');

(async () => {
  console.log('📸 Starting automated wireframe capture...\n');
  
  const browser = await puppeteer.launch({ 
    headless: false,
    defaultViewport: null,
    args: ['--start-maximized']
  });
  
  const page = await browser.newPage();
  
  try {
    // Set desktop viewport
    await page.setViewport({ width: 1920, height: 1080 });
    
    console.log('1️⃣  Capturing landing page...');
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle2', timeout: 10000 });
    await new Promise(resolve => setTimeout(resolve, 1000));
    await page.screenshot({ 
      path: 'wireframe_01_landing.png',
      fullPage: false 
    });
    console.log('   ✅ wireframe_01_landing.png\n');
    
    // Start new conversation
    console.log('2️⃣  Capturing customer selection...');
    try {
      await page.click('button', { timeout: 5000 });
      await new Promise(resolve => setTimeout(resolve, 1500));
      await page.screenshot({ 
        path: 'wireframe_02_customer_selection.png',
        fullPage: false 
      });
      console.log('   ✅ wireframe_02_customer_selection.png\n');
    } catch (e) {
      console.log('   ⚠️  Skipped (button not found)\n');
    }
    
    // Select first customer
    console.log('3️⃣  Capturing initial greeting...');
    try {
      const buttons = await page.$$('button');
      if (buttons.length > 1) {
        await buttons[1].click(); // Second button (first customer)
        await new Promise(resolve => setTimeout(resolve, 3000));
      }
      await page.screenshot({ 
        path: 'wireframe_03_initial_greeting.png',
        fullPage: false 
      });
      console.log('   ✅ wireframe_03_initial_greeting.png\n');
    } catch (e) {
      console.log('   ⚠️  Skipped (customer button not found)\n');
    }
    
    // Type "yes"
    console.log('4️⃣  Capturing user input...');
    try {
      const textarea = await page.$('textarea');
      if (textarea) {
        await textarea.type('yes', { delay: 100 });
        await new Promise(resolve => setTimeout(resolve, 500));
        await page.screenshot({ 
          path: 'wireframe_04_user_typing.png',
          fullPage: false 
        });
        console.log('   ✅ wireframe_04_user_typing.png\n');
        
        // Send message
        console.log('5️⃣  Capturing sales conversation...');
        const submitButton = await page.$('button[type="submit"]');
        if (submitButton) {
          await submitButton.click();
          await new Promise(resolve => setTimeout(resolve, 6000)); // Wait for AI response
        }
        await page.screenshot({ 
          path: 'wireframe_05_sales_conversation.png',
          fullPage: false 
        });
        console.log('   ✅ wireframe_05_sales_conversation.png\n');
      }
    } catch (e) {
      console.log('   ⚠️  Skipped (textarea not found)\n');
    }
    
    // Enter loan details
    console.log('6️⃣  Capturing loan details...');
    try {
      const textarea = await page.$('textarea');
      if (textarea) {
        await textarea.click({ clickCount: 3 }); // Select all
        await textarea.type('50000 for 12 months', { delay: 100 });
        await new Promise(resolve => setTimeout(resolve, 500));
        
        const submitButton = await page.$('button[type="submit"]');
        if (submitButton) {
          await submitButton.click();
          await new Promise(resolve => setTimeout(resolve, 6000));
        }
        await page.screenshot({ 
          path: 'wireframe_06_loan_details_collected.png',
          fullPage: false 
        });
        console.log('   ✅ wireframe_06_loan_details_collected.png\n');
      }
    } catch (e) {
      console.log('   ⚠️  Skipped (input error)\n');
    }
    
    // Click quick reply buttons if available
    console.log('7️⃣  Capturing verification stage...');
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const buttons = await page.$$('button');
      // Look for "Yes, Proceed" or similar
      for (let button of buttons) {
        const text = await page.evaluate(el => el.textContent, button);
        if (text.includes('Yes') || text.includes('Proceed')) {
          await button.click();
          await new Promise(resolve => setTimeout(resolve, 4000));
          break;
        }
      }
      await page.screenshot({ 
        path: 'wireframe_07_verification_stage.png',
        fullPage: false 
      });
      console.log('   ✅ wireframe_07_verification_stage.png\n');
    } catch (e) {
      console.log('   ⚠️  Partial capture\n');
    }
    
    // Continue to approval
    console.log('8️⃣  Capturing approval screen...');
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const buttons = await page.$$('button');
      for (let button of buttons) {
        const text = await page.evaluate(el => el.textContent, button);
        if (text.includes('Correct') || text.includes('Confirm')) {
          await button.click();
          await new Promise(resolve => setTimeout(resolve, 4000));
          break;
        }
      }
      await page.screenshot({ 
        path: 'wireframe_08_approval_screen.png',
        fullPage: false 
      });
      console.log('   ✅ wireframe_08_approval_screen.png\n');
    } catch (e) {
      console.log('   ⚠️  Partial capture\n');
    }
    
    // Sanction letter
    console.log('9️⃣  Capturing sanction letter...');
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const buttons = await page.$$('button');
      for (let button of buttons) {
        const text = await page.evaluate(el => el.textContent, button);
        if (text.includes('Generate') || text.includes('Sanction')) {
          await button.click();
          await new Promise(resolve => setTimeout(resolve, 3000));
          break;
        }
      }
      await page.screenshot({ 
        path: 'wireframe_09_sanction_letter.png',
        fullPage: false 
      });
      console.log('   ✅ wireframe_09_sanction_letter.png\n');
    } catch (e) {
      console.log('   ⚠️  Partial capture\n');
    }
    
    // Mobile view
    console.log('🔟 Capturing mobile view...');
    await page.setViewport({ width: 375, height: 812 });
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle2', timeout: 10000 });
    await new Promise(resolve => setTimeout(resolve, 1500));
    await page.screenshot({ 
      path: 'wireframe_10_mobile_view.png',
      fullPage: true 
    });
    console.log('   ✅ wireframe_10_mobile_view.png\n');
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 WIREFRAME CAPTURE COMPLETE!');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📁 Location: D:\\EY-Techathon\\Diagrams\\wireframe_*.png');
    console.log('📊 Total Screenshots: 10 (Desktop + Mobile views)');
    console.log('✅ Ready for PowerPoint insertion!');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
  } catch (error) {
    console.error('\n❌ Error during capture:', error.message);
    console.log('\n💡 Tip: Make sure both servers are running:');
    console.log('   Backend:  http://localhost:8000');
    console.log('   Frontend: http://localhost:5173');
  } finally {
    await browser.close();
  }
})();
