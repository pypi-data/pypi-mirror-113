Object.defineProperty(exports, "__esModule", { value: true });
function parseApiError(resp) {
    var detail = ((resp && resp.responseJSON) || {}).detail;
    // return immediately if string
    if (typeof detail === 'string') {
        return detail;
    }
    if (detail && detail.message) {
        return detail.message;
    }
    return 'Unknown API Error';
}
exports.default = parseApiError;
//# sourceMappingURL=parseApiError.jsx.map