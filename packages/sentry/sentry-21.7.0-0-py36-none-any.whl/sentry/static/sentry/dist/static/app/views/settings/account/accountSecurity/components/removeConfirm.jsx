Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var locale_1 = require("app/locale");
var confirmHeader_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/confirmHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var message = (<React.Fragment>
    <confirmHeader_1.default>{locale_1.t('Do you want to remove this method?')}</confirmHeader_1.default>
    <textBlock_1.default>
      {locale_1.t('Removing the last authentication method will disable two-factor authentication completely.')}
    </textBlock_1.default>
  </React.Fragment>);
var RemoveConfirm = function (props) { return <confirm_1.default {...props} message={message}/>; };
exports.default = RemoveConfirm;
//# sourceMappingURL=removeConfirm.jsx.map