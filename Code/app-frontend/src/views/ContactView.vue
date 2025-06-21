<template>
    <div class="wholepage">
    <div class="contact-page">
      <h2 class="contact-title">Contact Us</h2>
  
      <div class="contact-info">
        <p>Email: <a href="mailto:bookease31@gmail.com">bookease31@gmail.com</a></p>
        <p>Follow us on social media:</p>
        <div class="social-links">
          <button type="button" class="btn btn-dark btn-lg user-nav"><a href="#" class="social-link">Facebook</a></button>
          <button type="button" class="btn btn-dark btn-lg user-nav"><a href="#" class="social-link">Twitter</a></button>
          <button type="button" class="btn btn-dark btn-lg user-nav" ><a href="#" class="social-link">Instagram</a></button>
        </div>
        <hr>
        <img src="../assets/background.png" class="image">
      </div>
    </div>
</div>
  </template>
  
  <script>
  export default {
    name: 'ContactPage',
  };
  </script>
  
  <style scoped>

.image {
  min-height: 450px;
  width: 100%;
  background-color: #053544;
  margin: 0;
}

a{
    text-decoration: none;
    color: aquamarine;
}

  .contact-page {
    background-color: #053544;
    color: #ffffff;
    max-width: 100%;
    margin: 0 auto;
    padding: 20px;
  }
  .wholepage {
    background-color: #053544;
    max-width: 100%;
  }
  .contact-title {
    font-size: 32px;
    margin-bottom: 20px;
  }
  
  .contact-info {
    font-size: 16px;
    line-height: 1.5;
  }
  
  .social-links {
    display: flex;
    justify-content: center;
    justify-items: center;
  }
  
  .social-link {
    color: #ffffff;
    text-decoration: none;
    margin-right: 10px;


  }
  
  .social-link:last-child {
    margin-right: 0;
  }
  </style>
  