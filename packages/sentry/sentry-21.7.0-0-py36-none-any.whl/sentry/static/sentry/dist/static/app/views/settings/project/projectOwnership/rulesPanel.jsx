Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_autosize_textarea_1 = tslib_1.__importDefault(require("react-autosize-textarea"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var panels_1 = require("app/components/panels");
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var icons_1 = require("app/icons");
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RulesPanel = /** @class */ (function (_super) {
    tslib_1.__extends(RulesPanel, _super);
    function RulesPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RulesPanel.prototype.renderIcon = function (provider) {
        switch (provider) {
            case 'github':
                return <icons_1.IconGithub size="md"/>;
            case 'gitlab':
                return <icons_1.IconGitlab size="md"/>;
            default:
                return <icons_1.IconSentry size="md"/>;
        }
    };
    RulesPanel.prototype.renderTitle = function () {
        switch (this.props.type) {
            case 'codeowners':
                return 'CODEOWNERS';
            case 'issueowners':
                return 'Ownership Rules';
            default:
                return null;
        }
    };
    RulesPanel.prototype.render = function () {
        var _a = this.props, raw = _a.raw, dateUpdated = _a.dateUpdated, provider = _a.provider, repoName = _a.repoName, readOnly = _a.readOnly, placeholder = _a.placeholder, detail = _a.detail, controls = _a.controls, dataTestId = _a["data-test-id"];
        return (<Container data-test-id={dataTestId}>
        <RulesHeader>
          <TitleContainer>
            {this.renderIcon(provider !== null && provider !== void 0 ? provider : '')}
            <Title>{this.renderTitle()}</Title>
          </TitleContainer>
          {readOnly && <ReadOnlyTag type="default">{'Read Only'}</ReadOnlyTag>}
          {repoName && <Repository>{repoName}</Repository>}
          {detail && <Detail>{detail}</Detail>}
        </RulesHeader>
        <RulesView>
          <InnerPanel>
            <InnerPanelHeader>
              <SyncDate>
                {dateUpdated && "Last synced " + moment_1.default(dateUpdated).fromNow()}
              </SyncDate>
              <Controls>
                {(controls || []).map(function (c, n) { return (<span key={n}> {c}</span>); })}
              </Controls>
            </InnerPanelHeader>
            <InnerPanelBody>
              <StyledTextArea value={raw} spellCheck="false" autoComplete="off" autoCorrect="off" autoCapitalize="off" placeholder={placeholder}/>
            </InnerPanelBody>
          </InnerPanel>
        </RulesView>
      </Container>);
    };
    return RulesPanel;
}(React.Component));
exports.default = react_1.withTheme(RulesPanel);
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 2fr;\n  grid-template-areas: 'rules-header rules-view';\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 2fr;\n  grid-template-areas: 'rules-header rules-view';\n  margin-bottom: ", ";\n"])), space_1.default(3));
var RulesHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  grid-area: rules-header;\n  display: grid;\n  grid-template-columns: 2fr 1fr;\n  grid-template-rows: 45px 1fr 1fr 1fr 1fr;\n  grid-template-areas: 'title tag' 'repository repository' '. .' '. .' 'detail detail';\n  border: 1px solid ", ";\n  border-radius: 4px 0 0 4px;\n  border-right: none;\n  box-shadow: 0 2px 0 rgb(37 11 54 / 4%);\n  background-color: ", ";\n"], ["\n  grid-area: rules-header;\n  display: grid;\n  grid-template-columns: 2fr 1fr;\n  grid-template-rows: 45px 1fr 1fr 1fr 1fr;\n  grid-template-areas: 'title tag' 'repository repository' '. .' '. .' 'detail detail';\n  border: 1px solid ", ";\n  border-radius: 4px 0 0 4px;\n  border-right: none;\n  box-shadow: 0 2px 0 rgb(37 11 54 / 4%);\n  background-color: ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.background; });
var TitleContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-area: title;\n  align-self: center;\n  padding-left: ", ";\n  display: flex;\n  * {\n    padding-right: ", ";\n  }\n"], ["\n  grid-area: title;\n  align-self: center;\n  padding-left: ", ";\n  display: flex;\n  * {\n    padding-right: ", ";\n  }\n"])), space_1.default(2), space_1.default(0.5));
var Title = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  align-self: center;\n"], ["\n  align-self: center;\n"])));
var ReadOnlyTag = styled_1.default(tag_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  grid-area: tag;\n  align-self: center;\n  justify-self: end;\n  padding-right: ", ";\n"], ["\n  grid-area: tag;\n  align-self: center;\n  justify-self: end;\n  padding-right: ", ";\n"])), space_1.default(1));
var Repository = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  grid-area: repository;\n  padding-left: calc(", " + ", ");\n  color: ", ";\n  font-size: 14px;\n"], ["\n  grid-area: repository;\n  padding-left: calc(", " + ", ");\n  color: ", ";\n  font-size: 14px;\n"])), space_1.default(2), space_1.default(3), function (p) { return p.theme.textColor; });
var Detail = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  grid-area: detail;\n  align-self: end;\n  padding: 0 ", " ", " ", ";\n  color: ", ";\n  font-size: 14px;\n  line-height: 1.4;\n"], ["\n  grid-area: detail;\n  align-self: end;\n  padding: 0 ", " ", " ", ";\n  color: ", ";\n  font-size: 14px;\n  line-height: 1.4;\n"])), space_1.default(2), space_1.default(2), space_1.default(2), function (p) { return p.theme.textColor; });
var RulesView = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  grid-area: rules-view;\n"], ["\n  grid-area: rules-view;\n"])));
var InnerPanel = styled_1.default(panels_1.Panel)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0px;\n  margin: 0px;\n  height: 100%;\n"], ["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0px;\n  margin: 0px;\n  height: 100%;\n"])));
var InnerPanelHeader = styled_1.default(panels_1.PanelHeader)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 2fr 1fr;\n  grid-template-areas: 'sync-date controis';\n  text-transform: none;\n  font-size: 16px;\n  font-weight: 400;\n"], ["\n  display: grid;\n  grid-template-columns: 2fr 1fr;\n  grid-template-areas: 'sync-date controis';\n  text-transform: none;\n  font-size: 16px;\n  font-weight: 400;\n"])));
var InnerPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  height: auto;\n"], ["\n  height: auto;\n"])));
var StyledTextArea = styled_1.default(react_autosize_textarea_1.default)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  ", ";\n  height: 350px !important;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  line-height: ", ";\n  border: none;\n  box-shadow: none;\n  padding: ", ";\n  color: transparent;\n  text-shadow: 0 0 0 #9386a0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border: none;\n    box-shadow: none;\n  }\n"], ["\n  ", ";\n  height: 350px !important;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  line-height: ", ";\n  border: none;\n  box-shadow: none;\n  padding: ", ";\n  color: transparent;\n  text-shadow: 0 0 0 #9386a0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border: none;\n    box-shadow: none;\n  }\n"])), function (p) { return input_1.inputStyles(p); }, function (p) { return p.theme.text.familyMono; }, space_1.default(3), space_1.default(2));
var SyncDate = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  grid-area: sync-date;\n"], ["\n  grid-area: sync-date;\n"])));
var Controls = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n"], ["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=rulesPanel.jsx.map