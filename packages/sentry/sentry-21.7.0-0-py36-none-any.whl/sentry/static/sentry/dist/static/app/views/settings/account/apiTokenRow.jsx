Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
function ApiTokenRow(_a) {
    var token = _a.token, onRemove = _a.onRemove;
    return (<StyledPanelItem>
      <Controls>
        <InputWrapper>
          <textCopyInput_1.default>
            {getDynamicText_1.default({ value: token.token, fixed: 'CI_AUTH_TOKEN' })}
          </textCopyInput_1.default>
        </InputWrapper>
        <button_1.default size="small" onClick={function () { return onRemove(token); }} icon={<icons_1.IconSubtract isCircled size="xs"/>}>
          {locale_1.t('Remove')}
        </button_1.default>
      </Controls>

      <Details>
        <ScopesWrapper>
          <Heading>{locale_1.t('Scopes')}</Heading>
          <ScopeList>{token.scopes.join(', ')}</ScopeList>
        </ScopesWrapper>
        <div>
          <Heading>{locale_1.t('Created')}</Heading>
          <Time>
            <dateTime_1.default date={getDynamicText_1.default({
            value: token.dateCreated,
            fixed: new Date(1508208080000), // National Pasta Day
        })}/>
          </Time>
        </div>
      </Details>
    </StyledPanelItem>);
}
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex-direction: column;\n  padding: ", ";\n"], ["\n  flex-direction: column;\n  padding: ", ";\n"])), space_1.default(2));
var Controls = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var InputWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  font-size: ", ";\n  flex: 1;\n  margin-right: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, space_1.default(1));
var Details = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  margin-top: ", ";\n"])), space_1.default(1));
var ScopesWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var ScopeList = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.4;\n"], ["\n  font-size: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var Time = styled_1.default('time')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.4;\n"], ["\n  font-size: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var Heading = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; }, space_1.default(1));
exports.default = ApiTokenRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=apiTokenRow.jsx.map