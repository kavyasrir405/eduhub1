from django.http import Http404
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse

from .models import Course,CustomUser,CartItem,Payment,Question,Feedback
from django.db import connection
from django.db.models import Sum
from .forms import create_user_form

@login_required
def home(request):
    
    return render(request,'home.html')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def login_user(request):
    if request.method== "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')

    
    return render(request,'login.html')

def register(request):
    form = create_user_form()

    if request.method == 'POST':
        form = create_user_form(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        

    context = {'form': form}
    return render(request, 'register.html', context)
@login_required
def upload(request):
    user_instance= request.user
    print(user_instance)
    
    print(user_instance.user_id)

    if request.method=="POST":
        instructor_id = request.user
        print(instructor_id)
        course_name=request.POST.get("courseName")
        
        category=request.POST.get('category')
        course_description=request.POST.get('courseDescription')
        #course_learnt=request.POST.get('')
        course_price=request.POST.get('coursePrice')
        course_img=request.FILES['courseImage']
        course_file=request.FILES['courseContent']
        topic1=request.POST.get('Topic1')
        topic2=request.POST.get('Topic2')
        topic3=request.POST.get('Topic3')
        topic4=request.POST.get('Topic4')
        course=Course(course_name=course_name, category=category,course_description=course_description,instructor_id=user_instance.user_id,course_price=course_price,course_image=course_img,course_content=course_file,course_topic1=topic1,course_topic2=topic2,course_topic3=topic3,course_topic4=topic4)
        course.save()
        #return redirect('teaching.html', course_id=course.course_id)
        return redirect('teaching', course_idee=course.course_id)       
    else:
        # Handle the case when the request method is not POST
        return render(request, 'upload.html')
    
@login_required
def teaching(request,course_idee=None):
    print("illeeeeeeee")
    user = request.user if request.user.is_authenticated else None
    user_courses = Course.objects.filter(instructor=request.user.user_id)
    
    if course_idee:
      
        current_course = get_object_or_404(Course, course_id=course_idee)
    else:
        
        current_course = None

    context = {
        'user': user,
        'user_courses': user_courses,
        'current_course': current_course
    }

    return render(request, 'teaching.html', context)
@login_required
def course_details(request, course_idee):
    
    user_instance = request.user
    course_instance = Course.objects.get(course_id=course_idee)
    q1 =""" SELECT
        course_name,
        category,
        course_description,
        course_price,
        course_id,
        
        home_CustomUser.first_name AS instructor_first_name,
        home_Customuser.last_name AS instructor_last_name
    FROM home_Course
    JOIN home_CustomUser ON home_Course.instructor_id = home_customuser.user_id
    WHERE home_Course.course_id = %s """
    inner_course_details=  Course.objects.raw(q1,[course_idee])
    
    if request.method=="POST":
        question=request.POST.get("ques")
        studentId=request.user
        if question:
            value=Question(student_id=studentId,question_text=question,is_answered=False,course_id=course_instance)
            value.save()
        else:
            messages.warning(request, 'Please enter a question.')

            return render(request, 'course_details.html', {'course': course_idee})


    # q2="""SELECT * 
    # FROM home_Payment 
    # WHERE user_id_id = %s AND course_id_id = %s"""
    # paid_course=  Course.objects.raw(q2,[user_instance.user_id,course_idee])
    paid_course = Payment.objects.filter(user_id=user_instance,course_id=course_instance)

    answered_ques=Question.objects.filter(is_answered=True)
    print(answer)
    if paid_course:
        if answered_ques:
        
            context={
                'inner_course_details': inner_course_details,
             'paid':True,
                'answers':answered_ques
            }
        else:
            context = {
            'inner_course_details': inner_course_details,
             'paid':True
        }
    else:
        context = {
            'inner_course_details': inner_course_details,
             'paid':False
        }
    print(context)
    
    
            
    return render(request, 'course_details.html', context)

from django.shortcuts import render, redirect
from .models import CustomUser, Course, CartItem
@login_required
def cart(request):
    if request.user.is_authenticated:
        user_instance = request.user
        cart_items = CartItem.objects.filter(user_id=user_instance)
        total_price = cart_items.aggregate(Sum('course_id__course_price'))['course_id__course_price__sum']
        # query = """
        #     SELECT 
        #         home_Course.course_id,
        #         home_Course.course_name,
        #         home_Course.category,
        #         home_Course.course_price,
        #         SUM(home_Course.course_price) AS total_price,
        #         home_CustomUser.first_name AS instructor_first_name,
        #         home_CustomUser.last_name AS instructor_last_name
        #     FROM 
        #         home_CartItem
        #     INNER JOIN 
        #         home_Course ON home_CartItem.course_id_id = home_Course.course_id
        #     INNER JOIN 
        #         home_CustomUser ON home_Course.instructor_id = home_CustomUser.user_id
        #     WHERE 
        #         home_CartItem.user_id_id = %s
        #     GROUP BY
        #         home_Course.course_id, home_Course.course_name, home_Course.category,
        #         home_Course.course_price,home_Customuser.first_name, home_Customuser.last_name;
        # """

        # with connection.cursor() as cursor:
        #     cursor.execute(query, [user_instance.user_id])
        #     cart_items = cursor.fetchall()

        return render(request, 'cart.html', {'cart_items': cart_items,'total_price': total_price})
    else:
        
        return redirect('login')


# def add_to_cart(request, course_idee):
#     if request.user.is_authenticated:
#         user_instance = request.user
#         course_instance = Course.objects.get(course_id=course_idee)

#         existing_cart_item = CartItem.objects.filter(user_id=user_instance, course_id=course_instance)

        
#         if existing_cart_item :
#             print("course is ther already in the cart ")

        
#         else:
#             cart_item = CartItem(user_id=user_instance, course_id=course_instance)
#             cart_item.save()

#         return redirect('cart')
#     else:
       
#         return redirect('login')

@login_required
def add_to_cart(request, course_idee):
    if request.user.is_authenticated:
        user_instance = request.user
        
        # # Retrieve the course instance using raw SQL query
        # q1 = """
        #     SELECT *
        #     FROM home_Course
        #     WHERE home_Course.course_id = %s
        # """
        # course_instance_query = Course.objects.raw(q1, [course_idee])
        # course_instance = next(iter(course_instance_query))

# # Check if the course is already in the cartusing sql query
        # q2 = """SELECT * FROM home_CartItem WHERE user_id_id = %s AND course_id_id = %s"""
        # existing_cart_item = CartItem.objects.raw(q2, [user_instance.user_id, course_idee])
        
        # # Check if the course is already in the cart

        q1= """
            SELECT *
            FROM home_CartItem
            WHERE user_id_id = %s AND course_id_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(q1, [user_instance.user_id, course_idee])
            existing_cart_item = cursor.fetchall()
       
        

        if existing_cart_item:
            messages.success(request, 'Course already added to the cart.')
    
        else:
    
            q2 = """
                INSERT INTO home_CartItem (user_id_id, course_id_id)
                VALUES (%s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(q2, [user_instance.user_id, course_idee])
                
            messages.success(request, 'Course successfully added to the cart.')

            return redirect('cart')

            

        return redirect('cart')
    else:
        return redirect('login')



@login_required    
def remove_from_cart(request, course_idee):
    if request.user.is_authenticated:
        user_instance = request.user
        # course = Course.objects.get(course_id=course_id)
        # CartItem.objects.filter(user=user, course=course).delete()
        q1= """
                DELETE FROM  home_CartItem 
                 WHERE user_id_id = %s AND course_id_id = %s
            """
        with connection.cursor() as cursor:
                cursor.execute(q1, [user_instance.user_id, course_idee])
        messages.success(request, 'Course successfully removed from the cart.')


        return redirect('cart')
    else:
        # Redirect to login or show a message

        return redirect('login')
@login_required   
def payment(request):
     
    if request.user.is_authenticated:
        user_instance = request.user

        q1= """
            SELECT *
            FROM home_CartItem
            WHERE user_id_id = %s 
        """
        with connection.cursor() as cursor:
            cursor.execute(q1, [user_instance.user_id])
            existing_cart_item = cursor.fetchall()
       
        

        if not existing_cart_item:
            print("No items in the cart")
            return redirect('home')
        
        
        for cart_item in existing_cart_item:
            q2 = """
                INSERT INTO home_Payment (user_id_id, course_id_id)
                VALUES (%s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(q2, [user_instance.user_id,  cart_item[1]])
            
        for cart_item in existing_cart_item:
            print("removed from cart checkour")
            q3= """
                    DELETE FROM  home_CartItem 
                    WHERE user_id_id = %s AND course_id_id = %s
           

                """
            with connection.cursor() as cursor:
                    cursor.execute(q3, [user_instance.user_id, cart_item[1] ])
            messages.success(request, 'Courses succefully bought')
        return redirect('learning')
        

    else:
        return redirect('login')       


@login_required
def learning(request):
    user_id = request.user
    bought_courses = Payment.objects.filter(user_id=user_id)
    

    return render(request, 'learning.html', {'bought_courses': bought_courses})

   
    
@login_required
def signout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('login'))
   




@login_required
def category(request, cat , **kwargs):
    print(cat)
    user_instance=request.user
    print(user_instance)
    
    q1 =""" SELECT * ,
        home_CustomUser.first_name AS instructor_first_name,
        home_Customuser.last_name AS instructor_last_name
    FROM home_Course
    JOIN home_CustomUser ON home_Course.instructor_id = home_customuser.user_id
    WHERE home_Course.category= %s
    """
    
    development_courses = Course.objects.raw(q1, [cat])
    # development_courses= Course.objects.filter(category=cat)
    print(development_courses.query)
    print("de ecxxx",list(development_courses))
    paid=[]

    for a in development_courses:  
        course_instance = get_object_or_404(Course, course_id=a.course_id)


        paid_course = Payment.objects.filter(user_id=user_instance, course_id=course_instance)

        if paid_course:
            paid.append(True)
            
        else:
            paid.append(False)
    print(paid)
    zipped_data = zip(development_courses, paid)

    context = {
        'zipped_data': zipped_data,
        'cate': cat,
    }

            
    # context = {
    #             'development_courses': development_courses,
    #             'cate': 'Development',
    #             'paid': paid
    #         }
    return render(request, 'development.html', context)
  
    

   

# def development(request):
    
#     q1 =""" SELECT *
#     FROM home_Course
   
#     WHERE home_Course.category= 'development' """

#     development_courses = Course.objects.raw(q1)
#   
    
#     context = {
#         'development_courses': development_courses,
#         'cate':'Development'

#     }

#     return render(request, 'development.html', context)




def question(request):
    teacher=request.user
    course_ids = Course.objects.filter(instructor=teacher).values_list('course_id', flat=True)
    unanswered_ques=Question.objects.filter(is_answered=False,course_id__in=course_ids)
    context={
        'unanswered_questions':unanswered_ques
    }
    return render(request, 'question.html', context)
def answer(request, ques_id):
    if request.method == 'POST':
        # Retrieve the question instance
        question = get_object_or_404(Question, question_id=ques_id, is_answered=False)

        # Update the answer_text field based on the submitted form data
        answer_text = request.POST.get('answer_text')
        if answer_text:
            question.answer_text = answer_text

        # Mark the question as answered
            question.is_answered = True

        # Save the changes to the database
            question.save()
            
            
        else:
            messages.warning(request, 'Please enter a answer.')
    teacher=request.user
    course_ids = Course.objects.filter(instructor=teacher).values_list('course_id', flat=True)
    unanswered_ques=Question.objects.filter(is_answered=False,course_id__in=course_ids)
    context={
        'unanswered_questions':unanswered_ques
    }
        



    # Your existing view logic for rendering the form goes here
    # ...

    return render( request,'question.html',context)

def feedback(request,courses_id):



    courseNow = get_object_or_404(Course, course_id=courses_id)

    if request.method == 'POST':
            feedbackText = request.POST.get('feedback_text')
            # cId=request.POST.get('course_id')
            print("save yake agilla")
            feed=Feedback(student=request.user,course=courseNow,feedback_text=feedbackText) 
            feed.save()
            messages.success(request, 'Feedback submitted!')

    all_feedback = Feedback.objects.filter(course=courseNow)

    return render(request, 'feedback.html',{"Course":courseNow, "all_feedback": all_feedback})






def instruct_feedback(request):
    teacher=request.user
    courses=Course.objects.filter(instructor=teacher).values_list('course_id', flat=True)
    feedbacks=Feedback.objects.filter(course_id__in=courses)

    context={
        "feedback_to":feedbacks
    }

    return render(request, 'instruct_feedback.html', context)



