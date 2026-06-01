// using API_Server;
// using Microsoft.EntityFrameworkCore;

// var builder = WebApplication.CreateBuilder(args);
// // הוספת ה-DbContext למערכת
// builder.Services.AddDbContext<AppDbContext>(options =>
//     options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// // הוספת שירותי CORS
// builder.Services.AddCors(options =>
// {
//     options.AddPolicy("AllowReact",
//         policy => policy.WithOrigins("http://localhost:5180")
//                         .AllowAnyMethod()
//                         .AllowAnyHeader());
// });
// builder.Services.AddControllers();
// builder.Services.AddAuthorization();
// var app = builder.Build();
// // חשוב: השורה הזו היא זו שמפעילה את ה-HTTPS
// //app.UseHttpsRedirection();
// app.UseCors("AllowReact");
// app.UseAuthorization();
// app.MapControllers();
// using (var scope = app.Services.CreateScope())
// {
//     var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
//     var tableNames = db.Model.GetEntityTypes().Select(t => t.GetTableName());
//     Console.WriteLine("--- הטבלאות שנמצאו במסד הנתונים: ---");
//     foreach (var name in tableNames)
//     {
//         Console.WriteLine(name);
//     }
// }
// app.Run();

// using API_Server.Models;
// using Microsoft.EntityFrameworkCore;

// namespace API_Server
// {

//     // השם של ה"מנהל" שלנו
//     public class AppDbContext : DbContext

//     {
       
//         // הקונסטרקטור הזה הוא מה שמאפשר ל-Visual Studio לחבר את ה"מנהל" למסד הנתונים
//         public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

//         // כאן אנחנו רושמים את כל ה"מדפים" (הטבלאות) שלנו
//         public DbSet<Student> Students { get; set; }
//         public DbSet<Course> Course { get; set; }
//         public DbSet<Video> Videos { get; set; }
//         public DbSet<Enrollment> Enrollments { get; set; }
//         public DbSet<User> Users { get; set; }
//         protected override void OnModelCreating(ModelBuilder modelBuilder)
//         {
//             modelBuilder.Entity<Course>()
//                 .HasOne(c => c.Coach)
//                 .WithMany(u => u.Courses)
//                 .HasForeignKey(c => c.CoachId);
//         }
//     }
// }