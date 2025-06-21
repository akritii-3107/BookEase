<template>
  <div class="about-page">
    <h2 class="about-title">About Bookease</h2>
    <img src="../assets/bookease-logo.png">
    <hr>
    <p class="about-description">

      Welcome to Bookease, your one-stop destination for entertainment booking
      and monthly entertainment reports. At Bookease, we believe in making your
      entertainment experiences seamless, enjoyable, and hassle-free. Our
      platform offers a range of features that cater to all your entertainment
      needs.
    </p>

    <div class="feature">
      <hr>
      <h3 class="feature-title">Booking Shows</h3>
      <p class="feature-description">
        Bookease provides a simple and efficient way to book shows for your
        favorite movies, concerts, theater performances, and more. With just a
        few clicks, you can reserve your seats and enjoy a delightful experience
        at your preferred venue. Whether you are planning a solo outing or a
        fun-filled group event, Bookease ensures a smooth booking process for
        all.
      </p>
    </div>

    <div class="feature">
      <h3 class="feature-title">Monthly Entertainment Report</h3>
      <p class="feature-description">
        Stay updated and informed with our exclusive monthly entertainment
        report. This comprehensive report highlights the latest entertainment
        trends, upcoming events, blockbuster releases, and much more. With
        Bookease, you'll never miss out on the most anticipated shows and
        events, making sure you're always ahead of the entertainment curve.
      </p>
    </div>

    <div class="feature">
      <h3 class="feature-title">Attractive User Interface</h3>
      <p class="feature-description">
        Our platform boasts an attractive user interface that is both intuitive
        and visually appealing. We have carefully designed our website using our
        brand colors to create a delightful and immersive user experience. The
        combination of shades like #053544, #0e9a99, #caeded, and white reflects
        our commitment to aesthetics and modern design principles.
      </p>
    </div>

    <div class="feature">
      <h3 class="feature-title">Secure and Reliable</h3>
      <p class="feature-description">
        At Bookease, we prioritize your security and privacy. Our platform
        employs state-of-the-art security measures to safeguard your personal
        information and ensure a safe transaction environment. Rest assured,
        your data is in trusted hands.
      </p>
    </div>

    <div class="feature">
      <h3 class="feature-title">User-Friendly Navigation</h3>
      <p class="feature-description">
        We understand the importance of a seamless browsing experience. With
        our user-friendly navigation, finding and booking your favorite shows
        becomes effortless. Explore the wide range of entertainment options,
        read reviews, and make informed choices in just a few clicks.
      </p>
    </div>

    <div class="feature">
      <h3 class="feature-title">Customer Support</h3>
      <p class="feature-description">
        Our dedicated customer support team is always ready to assist you. If
        you have any queries, concerns, or need help with bookings, feel free to
        reach out to us. We are here to make your entertainment journey smooth
        and memorable.
      </p>
    </div>

    <p class="about-conclusion">
      Join us at Bookease and embark on a journey of entertainment like never
      before. Enjoy the convenience of online booking, stay up-to-date with our
      monthly reports, and relish every moment of your entertainment endeavors.
    </p>

    <p class="about-signature">
      Let Bookease be your ultimate companion for all things entertainment!
    </p>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
};
</script>

<style scoped>
.about-page {
  max-width: 800px;
  background-color: #053544;
  margin: 0 auto;
  padding: 20px;
}

.about-title {
  color: #cbf3ff;
  font-size: 32px;
  margin-bottom: 20px;
}
.about-page img{
  max-width: 100%;
    height: 200px;
    display: block;
    margin: 0 auto;
}

hr{
  color: #ffffff;

}
.about-description {
  color: #ffffff;
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.feature-title {
  color: #b0ddeb;
  font-size: 24px;
  margin-bottom: 10px;
}

.feature-description {
  color: #a5ffff;
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.about-conclusion {
  color: #d5f5f5;
  font-size: 18px;
  margin-top: 30px;
  margin-bottom: 10px;
}

.about-signature {
  color: #053544;
  font-size: 20px;
  font-weight: bold;
}
</style>

