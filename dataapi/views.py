import os
import re

import pandas as pd
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UploadedFile
from .serializers import AllDataSerializer
from .serializers import UploadedFileSerializer


class FileUploadView(APIView):
    """ Загрузка файла авторизованным пользователем
    создаёться информация о колонках в файле """

    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)

        if file_serializer.is_valid():
            uploaded_file = request.FILES['file']

            file_extension = os.path.splitext(uploaded_file.name)[1]

            if file_extension.lower() != '.csv':
                return Response({'message': 'Файл не является CSV файлом.'}, status=status.HTTP_400_BAD_REQUEST)

            base_file_name, _ = os.path.splitext(uploaded_file.name)
            file_name = base_file_name + '.csv'

            if UploadedFile.objects.filter(file_name=file_name).exists():
                return Response({'message': 'Файл с таким именем уже загружен. Пожалуйста, выберите другое имя файла.'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                # Считываем содержимое файла
                file_content = uploaded_file.read()
                # Создаем экземпляр UploadedFile
                uploaded_file_instance = UploadedFile()
                # Сохраняем содержимое файла в экземпляре UploadedFile
                uploaded_file_instance.file.save(file_name, ContentFile(file_content))
                # Устанавливаем имя файла
                uploaded_file_instance.file_name = file_name
                # Анализируем содержимое файла
                df = pd.read_csv(ContentFile(file_content))
                columns_info = df.columns.tolist()
                # Устанавливаем информацию о колонках
                uploaded_file_instance.column_info = columns_info
                # Сохраняем экземпляр UploadedFile
                uploaded_file_instance.save()
            except Exception as e:
                return Response({'message': 'Ошибка анализа файла.', 'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Файл успешно загружен'}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileList(APIView):
    """ Вывод информации о всех файлах """

    permission_classes = [AllowAny]

    def get(self, request):
        files = UploadedFile.objects.exclude(column_info=None)

        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data)


class FileDetailView(APIView):
    """ Вывод информации о конкретном файле по его ID """

    permission_classes = [AllowAny]

    def get(self, request, file_id):
        try:
            file = UploadedFile.objects.get(id=file_id)

            if file.column_info is None:
                return Response({'message': 'Файл с указанным ID не содержит информации о колонках'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = UploadedFileSerializer(file)
            return Response(serializer.data)

        except UploadedFile.DoesNotExist:
            return Response({'message': 'Файл с указанным ID не найден'}, status=status.HTTP_404_NOT_FOUND)


class AllDataView(APIView):
    """ Вывод информации из нужного файла и нужных колонках и
    фильтрация его по символам """

    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = AllDataSerializer(data=request.data)

        if serializer.is_valid():
            file_id = serializer.validated_data['file_id']
            selected_columns = serializer.validated_data.get('columns')

            try:
                uploaded_file = UploadedFile.objects.get(id=file_id)

                if uploaded_file.file.size == 0:
                    return Response({'message': 'Файл пуст'}, status=status.HTTP_400_BAD_REQUEST)

                data = pd.read_csv(uploaded_file.file.path, delimiter=',', encoding='utf-8')

                if data.empty:
                    return Response({'message': 'Данные не загружены из файла'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                if selected_columns:
                    def is_valid_value(value):
                        return bool(re.match("^[0-9a-z]+$", str(value)))

                    filtered_data = data[selected_columns].applymap(is_valid_value)
                    filtered_data = data[filtered_data.all(axis=1)]
                else:
                    filtered_data = data

                data_json = filtered_data.to_json(orient='records')

                return Response({'data': data_json}, status=status.HTTP_200_OK)
            except UploadedFile.DoesNotExist:
                return Response({'message': 'Файл с указанным ID не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDeleteView(APIView):
    """ Удаление файла по его ID """

    permission_classes = [IsAuthenticated, ]

    def delete(self, request, file_id):
        try:
            file = UploadedFile.objects.get(id=file_id)
            file.delete()
            return Response({'message': 'Файл успешно удален'}, status=status.HTTP_204_NO_CONTENT)

        except UploadedFile.DoesNotExist:
            return Response({'message': 'Файл с указанным ID не найден'}, status=status.HTTP_404_NOT_FOUND)