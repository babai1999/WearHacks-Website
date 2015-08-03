from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext_lazy as __
from django.forms.utils import ValidationError
    
class PDFField(forms.FileField):
    """
    Modified from https://djangosnippets.org/snippets/1189/
    """
    default_error_messages = {
        'invalid': _(u"No file was submitted."), #" Check the encoding type on the form."),
        'missing': _(u"No file was submitted."),
        'empty': _(u"The submitted file is empty."),
        'not_valid': _(u"Upload a valid document. The file you uploaded appears to be corrupted."),
        'not_pdf': _(u"Not a PDF file."),
        'file_size': _(u"Please keep file size under %(max_file_size)s. Current filesize %(current_file_size)s"),
        'sever_error': _(u"There was an issue uploading your file. Try to submit again."),

    }

    max_upload_size = 2621440 # 2MB
    content_types = ['application/pdf']

    def clean(self, data, initial=None):
        super(forms.FileField, self).clean(initial or data)
        if not data:
            return data
      
        file = data.file
        try:
            if not file.readable:
                raise ValidationError(self.error_messages['not_valid'])
            if data._size > self.max_upload_size:
                raise forms.ValidationError(self.error_messages['file_size'],
                    params = {
                     max_file_size: filesizeformat(self.max_upload_size), 
                     current_file_size: filesizeformat(data._size)
                    })
            try:
                from pyPdf import PdfFileReader
                PdfFileReader(file)
            except Exception as e:
                print str(e)
                raise ValidationError(self.error_messages['not_pdf'])
        except ValidationError, e:
            raise e
        except Exception, e:
            print str(e)
            raise forms.ValidationError(self.error_messages['sever_error'])
        return data

def get_registration_button_html():
    html = """
    <div class="row"><div class="col-xs-12 col-sm-7 col-sm-offset-3 text-center checkout-wrapper">
        <span id="registration-error" class="help-block hide message message-error">
            <strong>%(registration_failure_message)s</strong>
        </span>
        <a id="register" class="registration-form-action register-action mobile btn btn-lg btn-block btn-primary">
            <i class="fa fa-lock hide"></i><i class="fa fa-paper-plane"></i><i class="fa fa-spinner fa-pulse hide"></i><i class="fa fa-check hide"></i> 
        <span class="text">%(register)s</span></a>
        <span id="server-error" class="help-block hide message message-error"><
            strong>%(temporary_server_problem)s</strong>
        </span>
        <span id="checkout-error" class="help-block hide message message-error">
            <strong>%(checkout_failure_message)s</strong>
        </span>
        <span id="success-message" class="help-block hide message message-success">
            <strong>%(success_message)s</strong>
        </span>
        <a id="checkout" class="registration-form-action checkout-action mobile disabled btn btn-lg btn-block btn-primary">
            <i class="fa fa-lock"></i><i class="fa fa-unlock hide"></i><i class="fa fa-paper-plane hide"></i><i class="fa fa-spinner fa-pulse hide"></i><i class="fa fa-check hide"></i> 
        <span class="text">%(checkout)s</span></a>
        <a id="checkout" class="registration-form-action checkout-action register-action desktop btn btn-lg btn-block btn-primary">
            <i class="fa fa-lock"></i><i class="fa fa-paper-plane hide"></i><i class="fa fa-spinner fa-pulse hide"></i><i class="fa fa-check hide"></i> 
            <span class="text">%(checkout)s</span>
        </a>
        <p id="hint_checkout" class="has-info help-block">%(payment_handled_by_stripe)s</p>
    </div>
    </div>
    """

    html = html % {
        'registration_failure_message': _('Registration Failure Message'),
        'register': _('Register'),
        'temporary_server_problem': _('Temporary problem with our server'),
        'checkout_failure_message': _('Checkout Failure Message'),
        'success_message': _('Success'),
        'checkout': _('Checkout'),
        'payment_handled_by_stripe': _('Payment is handled by <a target="_blank" href="https://stripe.com/ca">Stripe</a>. We do not have acces to your card information.')
        }
    # __('Placeholder value'

    return html





