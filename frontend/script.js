// document.addEventListener("DOMContentLoaded", () => {
//   const badge = document.querySelector(".badge");
//   const unreadCount = document.querySelectorAll("#notifications-list li").length;
//   badge.textContent = unreadCount;

//   const markAsReadButtons = document.querySelectorAll(".mark-as-read");
//   markAsReadButtons.forEach((button) => {
//       button.addEventListener("click", () => {
//           const parentLi = button.parentElement;
//           parentLi.remove();
//           const updatedUnreadCount = document.querySelectorAll("#notifications-list li").length;
//           badge.textContent = updatedUnreadCount;
//       });
//   });
// });
