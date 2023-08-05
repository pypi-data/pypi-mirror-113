Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var selectField_1 = tslib_1.__importDefault(require("app/components/forms/selectField"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var selectOwners_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/selectOwners"));
var initialState = {
    text: '',
    tagName: '',
    type: 'path',
    owners: [],
    isValid: false,
};
function getMatchPlaceholder(type) {
    switch (type) {
        case 'path':
            return 'src/example/*';
        case 'url':
            return 'https://example.com/settings/*';
        case 'tag':
            return 'tag-value';
        default:
            return '';
    }
}
var RuleBuilder = /** @class */ (function (_super) {
    tslib_1.__extends(RuleBuilder, _super);
    function RuleBuilder() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.checkIsValid = function () {
            _this.setState(function (state) { return ({
                isValid: !!state.text && state.owners && !!state.owners.length,
            }); });
        };
        _this.handleTypeChange = function (val) {
            _this.setState({ type: val }); // TODO(ts): Add select value type as generic to select controls
            _this.checkIsValid();
        };
        _this.handleTagNameChangeValue = function (e) {
            _this.setState({ tagName: e.target.value }, _this.checkIsValid);
        };
        _this.handleChangeValue = function (e) {
            _this.setState({ text: e.target.value });
            _this.checkIsValid();
        };
        _this.handleChangeOwners = function (owners) {
            _this.setState({ owners: owners });
            _this.checkIsValid();
        };
        _this.handleAddRule = function () {
            var _a = _this.state, type = _a.type, text = _a.text, tagName = _a.tagName, owners = _a.owners, isValid = _a.isValid;
            if (!isValid) {
                indicator_1.addErrorMessage('A rule needs a type, a value, and one or more issue owners.');
                return;
            }
            var ownerText = owners
                .map(function (owner) {
                var _a;
                return owner.actor.type === 'team'
                    ? "#" + owner.actor.name
                    : (_a = memberListStore_1.default.getById(owner.actor.id)) === null || _a === void 0 ? void 0 : _a.email;
            })
                .join(' ');
            var quotedText = text.match(/\s/) ? "\"" + text + "\"" : text;
            var rule = (type === 'tag' ? "tags." + tagName : type) + ":" + quotedText + " " + ownerText;
            _this.props.onAddRule(rule);
            _this.setState(initialState);
        };
        _this.handleSelectCandidate = function (text, type) {
            _this.setState({ text: text, type: type });
            _this.checkIsValid();
        };
        return _this;
    }
    RuleBuilder.prototype.render = function () {
        var _this = this;
        var _a = this.props, urls = _a.urls, paths = _a.paths, disabled = _a.disabled, project = _a.project, organization = _a.organization;
        var _b = this.state, type = _b.type, text = _b.text, tagName = _b.tagName, owners = _b.owners, isValid = _b.isValid;
        return (<React.Fragment>
        {(paths || urls) && (<Candidates>
            {paths &&
                    paths.map(function (v) { return (<RuleCandidate key={v} onClick={function () { return _this.handleSelectCandidate(v, 'path'); }}>
                  <StyledIconAdd isCircled/>
                  <StyledTextOverflow>{v}</StyledTextOverflow>
                  <TypeHint>[PATH]</TypeHint>
                </RuleCandidate>); })}
            {urls &&
                    urls.map(function (v) { return (<RuleCandidate key={v} onClick={function () { return _this.handleSelectCandidate(v, 'url'); }}>
                  <StyledIconAdd isCircled/>
                  <StyledTextOverflow>{v}</StyledTextOverflow>
                  <TypeHint>[URL]</TypeHint>
                </RuleCandidate>); })}
          </Candidates>)}
        <BuilderBar>
          <BuilderSelect name="select-type" value={type} onChange={this.handleTypeChange} options={[
                { value: 'path', label: locale_1.t('Path') },
                { value: 'tag', label: locale_1.t('Tag') },
                { value: 'url', label: locale_1.t('URL') },
            ]} style={{ width: 140 }} clearable={false} disabled={disabled}/>
          {type === 'tag' && (<BuilderTagNameInput value={tagName} onChange={this.handleTagNameChangeValue} disabled={disabled} placeholder="tag-name"/>)}
          <BuilderInput value={text} onChange={this.handleChangeValue} disabled={disabled} placeholder={getMatchPlaceholder(type)}/>
          <Divider direction="right"/>
          <SelectOwnersWrapper>
            <selectOwners_1.default organization={organization} project={project} value={owners} onChange={this.handleChangeOwners} disabled={disabled}/>
          </SelectOwnersWrapper>

          <AddButton priority="primary" disabled={!isValid} onClick={this.handleAddRule} icon={<icons_1.IconAdd isCircled/>} size="small"/>
        </BuilderBar>
      </React.Fragment>);
    };
    return RuleBuilder;
}(React.Component));
var Candidates = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 10px;\n"], ["\n  margin-bottom: 10px;\n"])));
var TypeHint = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.border; });
var StyledTextOverflow = styled_1.default(textOverflow_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var RuleCandidate = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  border: 1px solid ", ";\n  background-color: #f8fafd;\n  padding-left: 5px;\n  margin-bottom: 3px;\n  cursor: pointer;\n  overflow: hidden;\n  display: flex;\n  align-items: center;\n"], ["\n  font-family: ", ";\n  border: 1px solid ", ";\n  background-color: #f8fafd;\n  padding-left: 5px;\n  margin-bottom: 3px;\n  cursor: pointer;\n  overflow: hidden;\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.border; });
var StyledIconAdd = styled_1.default(icons_1.IconAdd)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-right: 5px;\n  flex-shrink: 0;\n"], ["\n  color: ", ";\n  margin-right: 5px;\n  flex-shrink: 0;\n"])), function (p) { return p.theme.border; });
var BuilderBar = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  height: 40px;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  height: 40px;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space_1.default(2));
var BuilderSelect = styled_1.default(selectField_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  width: 50px;\n  flex-shrink: 0;\n"], ["\n  margin-right: ", ";\n  width: 50px;\n  flex-shrink: 0;\n"])), space_1.default(1.5));
var BuilderInput = styled_1.default(input_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n"], ["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n"])), space_1.default(1), space_1.default(0.5));
var BuilderTagNameInput = styled_1.default(input_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n  width: 200px;\n"], ["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n  width: 200px;\n"])), space_1.default(1), space_1.default(0.5));
var Divider = styled_1.default(icons_1.IconChevron)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  flex-shrink: 0;\n  margin-right: 5px;\n"], ["\n  color: ", ";\n  flex-shrink: 0;\n  margin-right: 5px;\n"])), function (p) { return p.theme.border; });
var SelectOwnersWrapper = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"])), space_1.default(1));
var AddButton = styled_1.default(button_1.default)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  padding: ", "; /* this sizes the button up to align with the inputs */\n"], ["\n  padding: ", "; /* this sizes the button up to align with the inputs */\n"])), space_1.default(0.5));
exports.default = RuleBuilder;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=ruleBuilder.jsx.map