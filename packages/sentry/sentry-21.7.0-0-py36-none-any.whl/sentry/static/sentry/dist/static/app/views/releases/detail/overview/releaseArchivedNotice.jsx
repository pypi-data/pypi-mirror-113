Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
function ReleaseArchivedNotice(_a) {
    var onRestore = _a.onRestore, multi = _a.multi;
    return (<alert_1.default icon={<icons_1.IconInfo size="md"/>} type="warning">
      {multi
            ? locale_1.t('These releases have been archived.')
            : locale_1.t('This release has been archived.')}

      {!multi && onRestore && (<react_1.Fragment>
          {' '}
          <UnarchiveButton size="zero" priority="link" onClick={onRestore}>
            {locale_1.t('Restore this release')}
          </UnarchiveButton>
        </react_1.Fragment>)}
    </alert_1.default>);
}
var UnarchiveButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: inherit;\n  text-decoration: underline;\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  font-size: inherit;\n  text-decoration: underline;\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; });
exports.default = ReleaseArchivedNotice;
var templateObject_1;
//# sourceMappingURL=releaseArchivedNotice.jsx.map