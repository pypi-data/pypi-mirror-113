Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var RecoveryCodes = function (_a) {
    var className = _a.className, isEnrolled = _a.isEnrolled, codes = _a.codes, onRegenerateBackupCodes = _a.onRegenerateBackupCodes;
    var printCodes = function () {
        // eslint-disable-next-line dot-notation
        var iframe = window.frames['printable'];
        iframe.document.write(codes.join('<br>'));
        iframe.print();
        iframe.document.close();
    };
    if (!isEnrolled || !codes) {
        return null;
    }
    var formattedCodes = codes.join(' \n');
    return (<CodeContainer className={className}>
      <panels_1.PanelHeader hasButtons>
        {locale_1.t('Unused Codes')}

        <Actions>
          <clipboard_1.default hideUnsupported value={formattedCodes}>
            <button_1.default size="small" label={locale_1.t('copy')}>
              <icons_1.IconCopy />
            </button_1.default>
          </clipboard_1.default>
          <button_1.default size="small" onClick={printCodes} label={locale_1.t('print')}>
            <icons_1.IconPrint />
          </button_1.default>
          <button_1.default size="small" download="sentry-recovery-codes.txt" href={"data:text/plain;charset=utf-8," + formattedCodes} label={locale_1.t('download')}>
            <icons_1.IconDownload />
          </button_1.default>
          <confirm_1.default onConfirm={onRegenerateBackupCodes} message={locale_1.t('Are you sure you want to regenerate recovery codes? Your old codes will no longer work.')}>
            <button_1.default priority="danger" size="small">
              {locale_1.t('Regenerate Codes')}
            </button_1.default>
          </confirm_1.default>
        </Actions>
      </panels_1.PanelHeader>
      <panels_1.PanelBody>
        <panels_1.PanelAlert type="warning">
          {locale_1.t('Make sure to save a copy of your recovery codes and store them in a safe place.')}
        </panels_1.PanelAlert>
        <div>{!!codes.length && codes.map(function (code) { return <Code key={code}>{code}</Code>; })}</div>
        {!codes.length && (<emptyMessage_1.default>{locale_1.t('You have no more recovery codes to use')}</emptyMessage_1.default>)}
      </panels_1.PanelBody>
      <iframe name="printable" style={{ display: 'none' }}/>
    </CodeContainer>);
};
exports.default = RecoveryCodes;
var CodeContainer = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(4));
var Actions = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space_1.default(1));
var Code = styled_1.default(panels_1.PanelItem)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  padding: ", ";\n"], ["\n  font-family: ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.text.familyMono; }, space_1.default(2));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=recoveryCodes.jsx.map