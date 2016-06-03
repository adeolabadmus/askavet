|Travis Badge|

**This library allows you to quickly and easily use the SendGrid Web API
via Python.**

Currently this library supports our `v2 Mail
endpoint <https://sendgrid.com/docs/API_Reference/Web_API/mail.html>`__
and the `v3 Web
API <https://sendgrid.com/docs/API_Reference/Web_API_v3/index.html>`__.

Installation
============

``pip install sendgrid``

or

``easy_install sendgrid``

Dependencies
------------

-  The SendGrid Service, starting at the `free
   level <https://sendgrid.com/free?source=sendgrid-python>`__
-  `SMTAPI-Python <https://github.com/sendgrid/smtpapi-python>`__
-  `Python-HTTP-Client <https://github.com/sendgrid/python-http-client>`__

Environment Variables (for v3 Web API)
--------------------------------------

`Sample
.env <https://github.com/sendgrid/sendgrid-python/blob/python_http_client/.env_sample>`__,
please rename to ``.env`` and add your `SendGrid API
Key <https://app.sendgrid.com/settings/api_keys>`__, or you can pass
your API Key into the SendGridClient constructor.

Quick Start
===========

v2 Mail Send endpoint (Send an Email)
-------------------------------------

.. code:: python

    import sendgrid

    sg = sendgrid.SendGridClient('YOUR_SENDGRID_API_KEY')


    message = sendgrid.Mail()
    message.add_to('John Doe <john@email.com>')
    message.set_subject('Example')
    message.set_html('Body')
    message.set_text('Body')
    message.set_from('Doe John <doe@email.com>')
    status, msg = sg.send(message)
    print(status, msg)

    #or

    message = sendgrid.Mail(to='john@email.com', subject='Example', html='Body', text='Body', from_email='doe@email.com')
    status, msg = sg.send(message)
    print(status, msg)

v3 Web API endpoints
--------------------

.. code:: python

    import sendgrid

    sg = sendgrid.SendGridAPIClient(apikey='YOUR_SENDGRID_API_KEY')
    # You can also store your API key an .env variable 'SENDGRID_API_KEY'

    response = sg.client.api_keys.get()
    print(response.status_code)
    print(response.response_body)
    print(response.response_headers)

Announcements
=============

**BREAKING CHANGE as of 2016.03.01**

Version ``2.0.0`` is a breaking change for the **Web API v3 endpoints**.
The mail send endpoint is not affected by this update.

Version 2.0.0 brings you full support for all Web API v3 endpoints. We
have the following resources to get you started quickly:

-  `SendGrid
   Documentation <https://sendgrid.com/docs/API_Reference/Web_API_v3/index.html>`__
-  `Usage
   Documentation <https://github.com/sendgrid/sendgrid-python/blob/master/USAGE.md>`__
-  `Example
   Code <https://github.com/sendgrid/sendgrid-python/blob/master/examples>`__

Thank you for your continued support!

For the **v2 Mail Send Endpoint**, if you upgrade to version ``1.2.x``,
the ``add_to`` method behaves differently. In the past this method
defaulted to using the ``SMTPAPI`` header. Now you must explicitly call
the ``smtpapi.add_to`` method. More on the ``SMTPAPI`` section.

Roadmap
-------

`Milestones <https://github.com/sendgrid/sendgrid-python/milestones>`__

How to Contribute
-----------------

We encourage contribution to our libraries, please see our
`CONTRIBUTING <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md>`__
guide for details.

-  `Feature
   Request <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md#feature_request>`__
-  `Bug
   Reports <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md#submit_a_bug_report>`__
-  `Improvements to the
   Codebase <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md#improvements_to_the_codebase>`__

Usage
-----

-  `SendGrid
   Docs <https://sendgrid.com/docs/API_Reference/index.html>`__
-  `v2 Mail
   Send <https://github.com/sendgrid/sendgrid-python/blob/master/USAGE_v2.md>`__
-  `v3 Web
   API <https://github.com/sendgrid/sendgrid-python/blob/master/USAGE.md>`__
-  `Example
   Code <https://github.com/sendgrid/sendgrid-python/blob/master/examples>`__

Unsupported Libraries
---------------------

-  `Official and Unsupported SendGrid
   Libraries <https://sendgrid.com/docs/Integrate/libraries.html>`__

About
=====

.. |SendGrid Logo| image:: https://assets3.sendgrid.com/mkt/assets/logos\_brands/small/sglogo\_2015\_blue-9c87423c2ff2ff393ebce1ab3bd018a4.png
   :target: https://www.sendgrid.com


sendgrid-python is guided and supported by the SendGrid `Developer
Experience Team <mailto:dx@sendgrid.com>`__.

sendgrid-python is maintained and funded by SendGrid, Inc. The names and
logos for sendgrid-python are trademarks of SendGrid, Inc.

.. |Travis Badge| image:: https://travis-ci.org/sendgrid/sendgrid-python.svg?branch=master
   :target: https://travis-ci.org/sendgrid/sendgrid-python


