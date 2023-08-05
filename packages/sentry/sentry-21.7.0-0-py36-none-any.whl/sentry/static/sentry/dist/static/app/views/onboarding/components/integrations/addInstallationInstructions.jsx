Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
// TODO: Make dyanmic for other platforms/integrations
function AddInstallationInstructions() {
    return (<react_1.Fragment>
      <p>
        {locale_1.tct('The automated AWS Lambda setup will instrument your Lambda functions with Sentry error and performance monitoring without any code changes. We use CloudFormation Stack ([learnMore]) to create the Sentry role which gives us access to your AWS account.', {
            learnMore: (<externalLink_1.default href="https://aws.amazon.com/cloudformation/">
                {locale_1.t('Learn more about CloudFormation')}
              </externalLink_1.default>),
        })}
      </p>
      <p>
        {locale_1.tct('Just press the [addInstallation] button below and complete the steps in the popup that opens.', { addInstallation: <strong>{locale_1.t('Add Installation')}</strong> })}
      </p>
      <p>
        {locale_1.tct('If you don’t want to add CloudFormation stack to your AWS environment, press the [manualSetup] button instead.', { manualSetup: <strong>{locale_1.t('Manual Setup')}</strong> })}
      </p>
    </react_1.Fragment>);
}
exports.default = AddInstallationInstructions;
//# sourceMappingURL=addInstallationInstructions.jsx.map