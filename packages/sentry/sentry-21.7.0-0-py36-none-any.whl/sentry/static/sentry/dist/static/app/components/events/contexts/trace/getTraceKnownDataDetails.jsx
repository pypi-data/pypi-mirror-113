Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var utils_1 = require("app/components/quickTrace/utils");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/views/performance/transactionSummary/utils");
var types_1 = require("./types");
function getUserKnownDataDetails(data, type, event, organization) {
    switch (type) {
        case types_1.TraceKnownDataType.TRACE_ID: {
            var traceId = data.trace_id || '';
            if (!traceId) {
                return undefined;
            }
            if (!organization.features.includes('discover-basic')) {
                return {
                    subject: locale_1.t('Trace ID'),
                    value: traceId,
                };
            }
            return {
                subject: locale_1.t('Trace ID'),
                value: (<ButtonWrapper>
            <pre className="val">
              <span className="val-string">{traceId}</span>
            </pre>
            <StyledButton size="xsmall" to={utils_1.generateTraceTarget(event, organization)}>
              {locale_1.t('Search by Trace')}
            </StyledButton>
          </ButtonWrapper>),
            };
        }
        case types_1.TraceKnownDataType.SPAN_ID: {
            return {
                subject: locale_1.t('Span ID'),
                value: data.span_id || '',
            };
        }
        case types_1.TraceKnownDataType.PARENT_SPAN_ID: {
            return {
                subject: locale_1.t('Parent Span ID'),
                value: data.parent_span_id || '',
            };
        }
        case types_1.TraceKnownDataType.OP_NAME: {
            return {
                subject: locale_1.t('Operation Name'),
                value: data.op || '',
            };
        }
        case types_1.TraceKnownDataType.STATUS: {
            return {
                subject: locale_1.t('Status'),
                value: data.status || '',
            };
        }
        case types_1.TraceKnownDataType.TRANSACTION_NAME: {
            var eventTag = event === null || event === void 0 ? void 0 : event.tags.find(function (tag) {
                return tag.key === 'transaction';
            });
            if (!eventTag || typeof eventTag.value !== 'string') {
                return undefined;
            }
            var transactionName = eventTag.value;
            var to = utils_2.transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: transactionName,
                projectID: event.projectID,
                query: {},
            });
            if (!organization.features.includes('performance-view')) {
                return {
                    subject: locale_1.t('Transaction'),
                    value: transactionName,
                };
            }
            return {
                subject: locale_1.t('Transaction'),
                value: (<ButtonWrapper>
            <pre className="val">
              <span className="val-string">{transactionName}</span>
            </pre>
            <StyledButton size="xsmall" to={to}>
              {locale_1.t('View Summary')}
            </StyledButton>
          </ButtonWrapper>),
            };
        }
        default:
            return undefined;
    }
}
var ButtonWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space_1.default(0.75), space_1.default(0.5));
exports.default = getUserKnownDataDetails;
var templateObject_1, templateObject_2;
//# sourceMappingURL=getTraceKnownDataDetails.jsx.map