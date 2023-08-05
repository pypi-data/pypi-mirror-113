Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var effectiveDirectives_1 = tslib_1.__importDefault(require("./effectiveDirectives"));
var linkOverrides = { 'script-src': 'script-src_2' };
var CSPHelp = function (_a) {
    var key = _a.data.effective_directive;
    var getHelp = function () { return ({
        __html: effectiveDirectives_1.default[key],
    }); };
    var getLinkHref = function () {
        var baseLink = 'https://developer.mozilla.org/en-US/docs/Web/Security/CSP/CSP_policy_directives#';
        if (key in linkOverrides) {
            return "" + baseLink + linkOverrides[key];
        }
        return "" + baseLink + key;
    };
    var getLink = function () {
        var href = getLinkHref();
        return (<StyledExternalLink href={href}>
        {'developer.mozilla.org'}
        <icons_1.IconOpen size="xs" className="external-icon"/>
      </StyledExternalLink>);
    };
    return (<div>
      <h4>
        <code>{key}</code>
      </h4>
      <blockquote dangerouslySetInnerHTML={getHelp()}/>
      <StyledP>
        <span>{'\u2014 MDN ('}</span>
        <span>{getLink()}</span>
        <span>{')'}</span>
      </StyledP>
    </div>);
};
exports.default = CSPHelp;
var StyledP = styled_1.default('p')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n"], ["\n  text-align: right;\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n"])), space_1.default(0.25));
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n"], ["\n  display: inline-flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map