from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dog
from .forms import FeedingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def dogs_index(request):
  dogs = Dog.objects.all()
  return render(request, 'dogs/index.html', {
    'dogs': dogs
  })

def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  feeding_form = FeedingForm()
  return render(
    request,
    'dogs/detail.html',
    {'dog': dog, 'feeding_form': feeding_form}
  )

class DogCreate(CreateView):
  model = Dog
  fields = '__all__'
  # success_url = '/dogs/'

  # def get_success_url(self):
  #   return f'/dogs/{self.object.id}'

class DogUpdate(UpdateView):
  model = Dog
  # Let's disallow the renaming of a dog by
  # excluding the name field
  fields = ['breed', 'description', 'age']

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'

def add_feeding(request, dog_id):
  # create a FeedingForm instance using
  # the data that was submitted via the form
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # can't save the form/object to the db
    # until we've assigned a dog_id
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('detail', dog_id=dog_id)

