from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self) -> None:
        class LessonTestCase(APITestCase):
            def setUp(self):
                self.user = User.objects.create(email='user@example.com')
                self.course = Course.objects.create(title="Тестовый курс 1")
                self.lesson = Lesson.objects.create(title="Тесстовый урок 1 курса 1", course=self.course, owner=self.user)
                self.client.force_authenticate(user=self.user)

            def test_lesson_retrieve(self):
                url = reverse("materials:lesson-get", args=(self.lesson.pk,))
                response = self.client.get(url)
                data = response.json()
                self.assertEqual(
                    response.status_code, status.HTTP_200_OK
                )
                self.assertEqual(
                    data.get("title"), self.lesson.title
                )

            def test_lesson_create(self):
                url = reverse("materials:lesson-create")
                data = {
                    "title": "Проверка создания доп. тестового урока",
                    'course': self.course.pk
                }
                response = self.client.post(url, data)
                self.assertEqual(
                    response.status_code, status.HTTP_201_CREATED
                )
                self.assertEqual(
                    Lesson.objects.all().count(), 2
                )

            def test_lesson_update(self):
                url = reverse("materials:lesson-update", args=(self.lesson.pk,))
                data = {
                    "title": "Проверка обновления доп. тестового урока",
                    'course': self.course.pk
                }
                response = self.client.patch(url, data)
                data = response.json()
                self.assertEqual(
                    response.status_code, status.HTTP_200_OK
                )
                self.assertEqual(
                    data.get("title"), "Проверка обновления доп. тестового урока"
                )

            def test_lesson_delete(self):
                url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
                response = self.client.delete(url)
                self.assertEqual(
                    response.status_code, status.HTTP_204_NO_CONTENT
                )
                self.assertEqual(
                    Lesson.objects.all().count(), 0
                )

            def test_lesson_list(self):
                url = reverse('materials:lesson-list')
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, status.HTTP_200_OK
                )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example.com')
        self.course = Course.objects.create(title="Тестовый курс 1")
        self.lesson = Lesson.objects.create(
            title="Тестовый урок 1 курса 1",
            course=self.course,
            owner=self.user,
            material_link='https://www.youtube.com/watch?v=test'
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тест создания подписки"""
        url = reverse('materials:subscription_create')
        data = {
            'course_id': self.course.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(
            Subscription.objects.first().course, self.course
        )

    def test_subscription_delete(self):
        """Тест удаления подписки"""
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        url = reverse('materials:subscription_create')
        data = {
            'course_id': self.course.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertEqual(Subscription.objects.count(), 0)

    def test_subscription_toggle(self):
        """Тест переключения подписки (создание → удаление → создание)"""
        url = reverse('materials:subscription_create')
        data = {'course_id': self.course.pk}

        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['message'], 'подписка добавлена')
        self.assertEqual(Subscription.objects.count(), 1)

        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['message'], 'подписка удалена')
        self.assertEqual(Subscription.objects.count(), 0)

        response3 = self.client.post(url, data)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data['message'], 'подписка добавлена')
        self.assertEqual(Subscription.objects.count(), 1)