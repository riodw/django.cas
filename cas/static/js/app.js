// app.js

// https://ariera.github.io/2017/09/26/django-webpack-vue-js-setting-up-a-new-project-that-s-easy-to-develop-and-deploy-part-1.html
// https://medium.com/js-dojo/7-ways-to-define-a-component-template-in-vuejs-c04e0c72900d

var personal = {
  template: "<p>Personal</p>",
};
var subscriptions = {
  template: "<p>Subscriptions</p>",
};
var notifications = {
  template: "<p>Notifications</p>",
};
var privacy = {
  template: "<p>Privacy</p>",
};
var security = {
  template: "<p>Security</p>",
};
var accessibility = {
  template: "<p>Accessibility</p>",
};

var router = new VueRouter({
  routes: [
    {
      path: "/",
      redirect: { name: "personal.overview" },
    },
    {
      path: "/personal",
      component: personal,
      children: [
        {
          path: "",
          name: "personal",
          redirect: { name: "personal.overview" },
        },
        {
          path: "overview",
          name: "personal.overview",
        },
        {
          path: "address",
          name: "personal.address",
        },
        {
          path: "position",
          name: "personal.position",
        },
      ],
    },
    {
      path: "/subscriptions",
      name: "subscriptions",
      component: subscriptions,
    },
    {
      path: "/notifications",
      name: "notifications",
      component: notifications,
    },
    {
      path: "/privacy",
      name: "privacy",
      component: privacy,
    },
    {
      path: "/security",
      name: "security",
      component: security,
    },
    {
      path: "/accessibility",
      name: "accessibility",
      component: accessibility,
    },
  ],
});

var app = new Vue({
  router,
  el: "#account_view",
  data: {
    my: {
      name: {
        first: "Rio",
        last: "Weber",
      },
      email: "riodweber@gmail.com",
      phone: "610.417.5096",
      joined: "March 2015",
    },
    options: [
      {
        title: "Overview",
        icon: "person",
        link: "personal.overview",
      },
      {
        title: "Address",
        icon: "room",
        link: "personal.address",
      },
      {
        title: "Position",
        icon: "work",
        link: "personal.position",
      },
    ],
  },
});
