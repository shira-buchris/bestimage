using Microsoft.AspNetCore.Mvc;

namespace serverCs.Controllers
{
    public class ServerController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
