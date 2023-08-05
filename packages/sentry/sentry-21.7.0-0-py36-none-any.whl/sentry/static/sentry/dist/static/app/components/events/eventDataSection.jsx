Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionContents = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var styles_1 = require("app/components/events/styles");
var iconAnchor_1 = require("app/icons/iconAnchor");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var defaultProps = {
    wrapTitle: true,
    raw: false,
    isCentered: false,
    showPermalink: true,
};
var EventDataSection = /** @class */ (function (_super) {
    tslib_1.__extends(EventDataSection, _super);
    function EventDataSection() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.dataSectionDOMRef = React.createRef();
        return _this;
    }
    EventDataSection.prototype.componentDidMount = function () {
        var dataSectionDOM = this.dataSectionDOMRef.current;
        if (location.hash && dataSectionDOM) {
            var _a = tslib_1.__read(location.hash.split('#'), 2), hash = _a[1];
            try {
                var anchorElement = hash && dataSectionDOM.querySelector('div#' + hash);
                if (anchorElement) {
                    anchorElement.scrollIntoView();
                }
            }
            catch (_b) {
                // Since we're blindly taking the hash from the url and shoving
                // it into a querySelector, it's possible that this may
                // raise an exception if the input is invalid. So let's just ignore
                // this instead of blowing up.
                // e.g. `document.querySelector('div#=')`
                // > Uncaught DOMException: Failed to execute 'querySelector' on 'Document': 'div#=' is not a valid selector.
            }
        }
    };
    EventDataSection.prototype.render = function () {
        var _a = this.props, children = _a.children, className = _a.className, type = _a.type, title = _a.title, toggleRaw = _a.toggleRaw, raw = _a.raw, wrapTitle = _a.wrapTitle, actions = _a.actions, isCentered = _a.isCentered, showPermalink = _a.showPermalink;
        var titleNode = wrapTitle ? <h3>{title}</h3> : title;
        return (<styles_1.DataSection ref={this.dataSectionDOMRef} className={className || ''}>
        {title && (<SectionHeader id={type} isCentered={isCentered}>
            <Title>
              {showPermalink ? (<Permalink href={'#' + type} className="permalink">
                  <StyledIconAnchor />
                  {titleNode}
                </Permalink>) : (<div>{titleNode}</div>)}
            </Title>
            {type === 'extra' && (<buttonBar_1.default merged active={raw ? 'raw' : 'formatted'}>
                <button_1.default barId="formatted" size="xsmall" onClick={function () { return callIfFunction_1.callIfFunction(toggleRaw, false); }}>
                  {locale_1.t('Formatted')}
                </button_1.default>
                <button_1.default barId="raw" size="xsmall" onClick={function () { return callIfFunction_1.callIfFunction(toggleRaw, true); }}>
                  {locale_1.t('Raw')}
                </button_1.default>
              </buttonBar_1.default>)}
            {actions && <ActionContainer>{actions}</ActionContainer>}
          </SectionHeader>)}
        <exports.SectionContents>{children}</exports.SectionContents>
      </styles_1.DataSection>);
    };
    EventDataSection.defaultProps = defaultProps;
    return EventDataSection;
}(React.Component));
var Title = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledIconAnchor = styled_1.default(iconAnchor_1.IconAnchor)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: none;\n  position: absolute;\n  top: 4px;\n  left: -22px;\n"], ["\n  display: none;\n  position: absolute;\n  top: 4px;\n  left: -22px;\n"])));
var Permalink = styled_1.default('a')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  :hover ", " {\n    display: block;\n    color: ", ";\n  }\n"], ["\n  :hover ", " {\n    display: block;\n    color: ", ";\n  }\n"])), StyledIconAnchor, function (p) { return p.theme.gray300; });
var SectionHeader = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n  margin-bottom: ", ";\n\n  > * {\n    margin-bottom: ", ";\n  }\n\n  & h3,\n  & h3 a {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    color: ", ";\n  }\n\n  & h3 {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    padding: ", " 0;\n    margin-bottom: 0;\n    text-transform: uppercase;\n  }\n\n  & small {\n    color: ", ";\n    font-size: ", ";\n    margin-right: ", ";\n    margin-left: ", ";\n\n    text-transform: none;\n  }\n  & small > span {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n    font-weight: normal;\n  }\n\n  @media (min-width: ", ") {\n    & > small {\n      margin-left: ", ";\n      display: inline-block;\n    }\n  }\n\n  ", "\n\n  >*:first-child {\n    position: relative;\n    flex-grow: 1;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n  margin-bottom: ", ";\n\n  > * {\n    margin-bottom: ", ";\n  }\n\n  & h3,\n  & h3 a {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    color: ", ";\n  }\n\n  & h3 {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    padding: ", " 0;\n    margin-bottom: 0;\n    text-transform: uppercase;\n  }\n\n  & small {\n    color: ", ";\n    font-size: ", ";\n    margin-right: ", ";\n    margin-left: ", ";\n\n    text-transform: none;\n  }\n  & small > span {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n    font-weight: normal;\n  }\n\n  @media (min-width: ", ") {\n    & > small {\n      margin-left: ", ";\n      display: inline-block;\n    }\n  }\n\n  ", "\n\n  >*:first-child {\n    position: relative;\n    flex-grow: 1;\n  }\n"])), space_1.default(1), space_1.default(0.5), function (p) { return p.theme.gray300; }, space_1.default(0.75), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.5), space_1.default(0.5), function (p) { return p.theme.textColor; }, function (p) { return p.theme.border; }, function (props) { return props.theme.breakpoints[2]; }, space_1.default(1), function (p) {
    return p.isCentered && react_1.css(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n      align-items: center;\n      @media (max-width: ", ") {\n        display: block;\n      }\n    "], ["\n      align-items: center;\n      @media (max-width: ", ") {\n        display: block;\n      }\n    "])), p.theme.breakpoints[0]);
});
exports.SectionContents = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ActionContainer = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 0;\n  max-width: 100%;\n"], ["\n  flex-shrink: 0;\n  max-width: 100%;\n"])));
exports.default = EventDataSection;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=eventDataSection.jsx.map