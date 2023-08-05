Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var assembly_1 = require("app/components/events/interfaces/assembly");
var contextLine_1 = tslib_1.__importDefault(require("app/components/events/interfaces/contextLine"));
var frameRegisters_1 = tslib_1.__importDefault(require("app/components/events/interfaces/frameRegisters"));
var frameVariables_1 = tslib_1.__importDefault(require("app/components/events/interfaces/frameVariables"));
var openInContextLine_1 = require("app/components/events/interfaces/openInContextLine");
var stacktraceLink_1 = tslib_1.__importDefault(require("app/components/events/interfaces/stacktraceLink"));
var utils_1 = require("app/components/events/interfaces/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var Context = function (_a) {
    var _b, _c;
    var _d = _a.hasContextVars, hasContextVars = _d === void 0 ? false : _d, _e = _a.hasContextSource, hasContextSource = _e === void 0 ? false : _e, _f = _a.hasContextRegisters, hasContextRegisters = _f === void 0 ? false : _f, _g = _a.isExpanded, isExpanded = _g === void 0 ? false : _g, _h = _a.hasAssembly, hasAssembly = _h === void 0 ? false : _h, _j = _a.expandable, expandable = _j === void 0 ? false : _j, _k = _a.emptySourceNotation, emptySourceNotation = _k === void 0 ? false : _k, registers = _a.registers, components = _a.components, frame = _a.frame, event = _a.event, organization = _a.organization;
    if (!hasContextSource && !hasContextVars && !hasContextRegisters && !hasAssembly) {
        return emptySourceNotation ? (<div className="empty-context">
        <StyledIconFlag size="xs"/>
        <p>{locale_1.t('No additional details are available for this frame.')}</p>
      </div>) : null;
    }
    var getContextLines = function () {
        if (isExpanded) {
            return frame.context;
        }
        return frame.context.filter(function (l) { return l[0] === frame.lineNo; });
    };
    var contextLines = getContextLines();
    var startLineNo = hasContextSource ? frame.context[0][0] : undefined;
    return (<ol start={startLineNo} className={"context " + (isExpanded ? 'expanded' : '')}>
      {utils_2.defined(frame.errors) && (<li className={expandable ? 'expandable error' : 'error'} key="errors">
          {frame.errors.join(', ')}
        </li>)}

      {frame.context &&
            contextLines.map(function (line, index) {
                var isActive = frame.lineNo === line[0];
                var hasComponents = isActive && components.length > 0;
                return (<StyledContextLine key={index} line={line} isActive={isActive}>
              {hasComponents && (<errorBoundary_1.default mini>
                  <openInContextLine_1.OpenInContextLine key={index} lineNo={line[0]} filename={frame.filename || ''} components={components}/>
                </errorBoundary_1.default>)}
              {(organization === null || organization === void 0 ? void 0 : organization.features.includes('integrations-stacktrace-link')) &&
                        isActive &&
                        isExpanded &&
                        frame.inApp &&
                        frame.filename && (<errorBoundary_1.default customComponent={null}>
                    <stacktraceLink_1.default key={index} lineNo={line[0]} frame={frame} event={event}/>
                  </errorBoundary_1.default>)}
            </StyledContextLine>);
            })}

      {(hasContextRegisters || hasContextVars) && (<StyledClippedBox clipHeight={100}>
          {hasContextRegisters && (<frameRegisters_1.default registers={registers} deviceArch={(_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.device) === null || _c === void 0 ? void 0 : _c.arch}/>)}
          {hasContextVars && <frameVariables_1.default data={frame.vars || {}}/>}
        </StyledClippedBox>)}

      {hasAssembly && (<assembly_1.Assembly {...utils_1.parseAssembly(frame.package)} filePath={frame.absPath}/>)}
    </ol>);
};
exports.default = withOrganization_1.default(Context);
var StyledClippedBox = styled_1.default(clippedBox_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: 0;\n  margin-right: 0;\n\n  &:first-of-type {\n    margin-top: 0;\n  }\n\n  :first-child {\n    margin-top: -", ";\n  }\n\n  > *:first-child {\n    padding-top: 0;\n    border-top: none;\n  }\n"], ["\n  margin-left: 0;\n  margin-right: 0;\n\n  &:first-of-type {\n    margin-top: 0;\n  }\n\n  :first-child {\n    margin-top: -", ";\n  }\n\n  > *:first-child {\n    padding-top: 0;\n    border-top: none;\n  }\n"])), space_1.default(3));
var StyledIconFlag = styled_1.default(icons_1.IconFlag)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledContextLine = styled_1.default(contextLine_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: inherit;\n  padding: 0;\n  text-indent: 20px;\n  z-index: 1000;\n"], ["\n  background: inherit;\n  padding: 0;\n  text-indent: 20px;\n  z-index: 1000;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=context.jsx.map