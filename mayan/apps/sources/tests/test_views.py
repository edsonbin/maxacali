from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase, override_settings

from acls.models import AccessControlList
from documents.models import Document, DocumentType, NewVersionBlock
from documents.permissions import permission_document_create
from documents.tests import (
    TEST_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_DESCRIPTION,
    TEST_DOCUMENT_TYPE
)
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME,
    TEST_USER_PASSWORD, TEST_USER_USERNAME
)
from ..links import link_upload_version
from ..literals import SOURCE_CHOICE_WEB_FORM
from ..models import WebFormSource

TEST_SOURCE_LABEL = 'test'
TEST_SOURCE_UNCOMPRESS = 'n'


class DocumentUploadTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentUploadTestCase, self).setUp()
        self.source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS
        )

        self.document.delete()

    def test_upload_wizard_without_permission(self):
        self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        with open(TEST_DOCUMENT_PATH) as file_object:
            response = self.client.post(
                reverse(
                    'sources:upload_interactive', args=(self.source.pk,)
                ), data={
                    'source-file': file_object,
                    'document_type_id': self.document_type.pk,
                }
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Document.objects.count(), 0)

    def test_upload_wizard_with_permission(self):
        self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        self.role.permissions.add(
            permission_document_create.stored_permission
        )

        with open(TEST_DOCUMENT_PATH) as file_object:
            response = self.client.post(
                reverse(
                    'sources:upload_interactive', args=(self.source.pk,)
                ), data={
                    'source-file': file_object,
                    'document_type_id': self.document_type.pk,
                }, follow=True
            )

        self.assertTrue(b'queued' in response.content)
        self.assertEqual(Document.objects.count(), 1)

    def test_upload_wizard_with_document_type_access(self):
        """
        Test uploading of documents by granting the document create
        permssion for the document type to the user
        """

        self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        # Create an access control entry giving the role the document
        # create permission for the selected document type.
        acl = AccessControlList.objects.create(
            content_object=self.document_type, role=self.role
        )
        acl.permissions.add(permission_document_create.stored_permission)

        with open(TEST_DOCUMENT_PATH) as file_object:
            response = self.client.post(
                reverse(
                    'sources:upload_interactive', args=(self.source.pk,)
                ), data={
                    'source-file': file_object,
                    'document_type_id': self.document_type.pk,
                }, follow=True
            )

        self.assertTrue(b'queued' in response.content)
        self.assertEqual(Document.objects.count(), 1)


@override_settings(OCR_AUTO_OCR=False)
class DocumentUploadIssueTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()

    def tearDown(self):
        self.document_type.delete()

    def test_issue_25(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        # Create new webform source
        self.client.post(
            reverse(
                'sources:setup_source_create', args=(SOURCE_CHOICE_WEB_FORM,)
            ), {'label': 'test', 'uncompress': 'n', 'enabled': True}
        )
        self.assertEqual(WebFormSource.objects.count(), 1)

        # Upload the test document
        with open(TEST_SMALL_DOCUMENT_PATH) as file_descriptor:
            self.client.post(
                reverse('sources:upload_interactive'),
                {
                    'document-language': 'eng', 'source-file': file_descriptor,
                    'document_type_id': self.document_type.pk
                }
            )
        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()
        # Test for issue 25 during creation
        # ** description fields was removed from upload from **
        self.assertEqual(document.description, '')

        # Reset description
        document.description = TEST_DOCUMENT_DESCRIPTION
        document.save()
        self.assertEqual(document.description, TEST_DOCUMENT_DESCRIPTION)

        # Test for issue 25 during editing
        self.client.post(
            reverse('documents:document_edit', args=(document.pk,)),
            {
                'description': TEST_DOCUMENT_DESCRIPTION,
                'language': document.language, 'label': document.label
            }
        )
        # Fetch document again and test description
        document = Document.objects.first()
        self.assertEqual(document.description, TEST_DOCUMENT_DESCRIPTION)


class NewDocumentVersionViewTestCase(GenericDocumentViewTestCase):
    def test_new_version_block(self):
        """
        Gitlab issue #231
        User shown option to upload new version of a document even though it
        is blocked by checkout - v2.0.0b2

        Expected results:
            - Link to upload version view should not resolve
            - Upload version view should reject request
        """

        self.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        NewVersionBlock.objects.block(self.document)

        response = self.post(
            'sources:upload_version', args=(self.document.pk,),
            follow=True
        )

        self.assertContains(
            response, text='blocked from uploading',
            status_code=200
        )

        response = self.get(
            'documents:document_version_list', args=(self.document.pk,),
            follow=True
        )

        # Needed by the url view resolver
        response.context.current_app = None
        resolved_link = link_upload_version.resolve(context=response.context)

        self.assertEqual(resolved_link, None)