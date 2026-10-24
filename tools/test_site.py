import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('privacy_site', Path(__file__).with_name('site.py'))
site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(site)


class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.content = json.loads((site.ROOT / 'content.json').read_text(encoding='utf-8'))
        self.content['configuration'] = dict(developerName='', supportEmail='', privacyPolicyURL='', supportURL='')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'public').mkdir()
        shutil.copyfile(site.ROOT / 'public/styles.css', self.root / 'public/styles.css')

    def write_pages(self):
        for name, text in site.render(self.content).items():
            (self.root / 'public' / name).write_text(text, encoding='utf-8')

    def configure(self):
        self.content['configuration'] = dict(developerName='Example & Co', supportEmail='help+app@example.org',
            privacyPolicyURL='https://example-owner.github.io/violin-support/privacy.html',
            supportURL='https://example-owner.github.io/violin-support/support.html')
        return dict(githubOwner='example-owner', repositoryName='violin-support')

    def test_incomplete_draft_stays_viewable_but_cannot_publish(self):
        self.write_pages()
        self.assertEqual(site.check_site(self.root, self.content), [])
        self.assertEqual(len(site.publication_errors(self.content, {})), 6)
        for name, text in site.render(self.content).items():
            self.assertIn('name="robots" content="noindex"', text)
            self.assertNotIn('mailto:', text)

    def test_complete_project_configuration_and_escaped_contact(self):
        deployment = self.configure()
        self.write_pages()
        self.assertEqual(site.publication_errors(self.content, deployment, 'example-owner/violin-support'), [])
        self.assertEqual(site.check_site(self.root, self.content), [])
        text = (self.root / 'public/support.html').read_text(encoding='utf-8')
        self.assertIn('Example &amp; Co', text)
        self.assertIn('mailto:help+app@example.org?subject=Violin+Trainer+Support', text)
        self.assertNotIn('name="robots"', text)

    def test_wrong_repository_and_urls_block_publication(self):
        deployment = self.configure()
        self.assertTrue(site.publication_errors(self.content, deployment, 'another-owner/violin-support'))
        for url in ('https://example-owner.github.io/privacy.html', 'http://example-owner.github.io/violin-support/privacy.html',
                    'https://example-owner.github.io/violin-support/privacy.html?draft=1', 'https://username:password@example.org/privacy.html'):
            self.content['configuration']['privacyPolicyURL'] = url
            self.assertTrue(site.publication_errors(self.content, deployment))

    def test_user_site_root_supported_without_project_prefix(self):
        self.configure()
        deployment = dict(githubOwner='example-owner', repositoryName='example-owner.github.io')
        self.content['configuration']['privacyPolicyURL'] = 'https://example-owner.github.io/privacy.html'
        self.content['configuration']['supportURL'] = 'https://example-owner.github.io/support.html'
        self.assertEqual(site.publication_errors(self.content, deployment), [])

    def test_extra_file_and_symlink_never_enter_public_artifact(self):
        self.write_pages()
        extra = self.root / 'public/private-recording.caf'
        extra.write_bytes(b'synthetic fixture, no audio')
        self.assertTrue(site.check_site(self.root, self.content))
        extra.unlink()
        css = self.root / 'public/styles.css'
        css.unlink()
        css.symlink_to(site.ROOT / 'public/styles.css')
        self.assertTrue(site.check_site(self.root, self.content))

    def test_broken_navigation_and_external_resources_are_rejected(self):
        self.write_pages()
        page = self.root / 'public/privacy.html'
        page.write_text(page.read_text(encoding='utf-8') + '<a href="missing.html">Broken</a><script src="https://example.org/tracker.js"></script>', encoding='utf-8')
        errors = site.check_site(self.root, self.content)
        self.assertTrue(any('Broken/non-relative' in e for e in errors))
        self.assertTrue(any('active/embedded' in e for e in errors))
        self.assertTrue(any('Unexpected external resource' in e for e in errors))

    def test_invalid_mail_address_is_not_published(self):
        for email in ('help@example.org?bcc=someone@example.org', 'mailto:help@example.org', 'not-an-email'):
            self.content['configuration']['supportEmail'] = email
            self.assertEqual(site.public_details(self.content['configuration'])['supportEmail'], '')
            self.assertNotIn('mailto:', site.render(self.content)['support-en.html'])

    def test_null_details_and_linked_public_directory_fail_closed(self):
        self.content['configuration']['developerName'] = None
        self.assertEqual(site.public_details(self.content['configuration'])['developerName'], '')
        public = self.root / 'public'
        shutil.rmtree(public)
        public.symlink_to(site.ROOT / 'public', target_is_directory=True)
        self.assertTrue(site.check_site(self.root, self.content))

    def test_changed_content_requires_regeneration(self):
        self.write_pages()
        updated = copy.deepcopy(self.content)
        updated['translations']['en']['privacy']['introduction'] += ' Updated policy.'
        self.assertIn('Outdated generated page: privacy-en.html', site.check_site(self.root, updated))


if __name__ == '__main__':
    unittest.main()
