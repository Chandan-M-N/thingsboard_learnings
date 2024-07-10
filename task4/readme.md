# Using Other Language Support in ThingsBoard

## Overview

ThingsBoard provides support for multiple languages in its Professional Edition. This readme guide outlines how to enable and customize language support for your ThingsBoard dashboard.

### Prerequisites

1. **ThingsBoard Edition**: Ensure you are using the Professional Edition of ThingsBoard, as language support is only available in this version.
   
### Steps to Enable and Customize Language Support

1. **Accessing Language Support Features**:
   
   - Language support in ThingsBoard is available through the Professional Edition, which allows users to configure their dashboard and widgets in different languages.

2. **Language Coverage**:

   - Currently, Spanish language support in ThingsBoard covers approximately 70% of the user interface text. The remaining 30% can be manually translated by users if they have access to the Professional Edition.

3. **Custom Translations**:

   - Users can provide custom translations for specific text elements within their dashboard and widgets. Here’s how you can add custom translations in the JSON format:

     ```json
     {
       "home": {
         "home": "Pagina principale di un sito web"
       },
       "custom": {
         "group": {
           "office": "Clienti di Office 1"
         },
         "my-dashboard": {
           "title": "Dashboard per esempi"
         },
         "my-widget": {
           "name": "Widget per dispositivo sensore",
           "label-text": "Etichetta per dispositivo sensore",
           "temperature": "Etichetta della temperatura",
           "low-temperature": "Bassa temperatura",
           "high-temperature": "Alta temperatura",
           "normal-temperature": "Temperatura normale"
         }
       }
     }
     ```

     - Replace the values with your desired translations for each key. This JSON structure allows you to define translations for different components of your dashboard and widgets.

4. **Dashboard Editing Mode**:

   - To apply custom translations within your dashboard, enter the editing mode and set the translation using the `{i18n}` format. For example:
   
     ```plaintext
     {i18n:custom.my-dashboard.title}
     ```
   
     This will display the dashboard title based on the translation provided in your custom JSON file.

5. **Advanced Translation Options**:

   - ThingsBoard also provides advanced options to translate dashboard and widget names, ensuring a fully localized user experience.

6. **Additional Resources**:

   - For more detailed instructions and examples, refer to the [ThingsBoard Custom Translation Documentation](https://thingsboard.io/docs/pe/user-guide/custom-translation/).

